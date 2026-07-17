import tkinter as tk
from tkinter import ttk, messagebox

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# =========================================================
# 1. 基本設定
# =========================================================

STEPS = 500
START_POSITION = "TV"
SEED = 10

# 初期速度。単位はミリ秒
INITIAL_INTERVAL = 200


# =========================================================
# 2. 状態と遷移確率行列
# =========================================================

states = [
    "Chabudai",
    "Husuma",
    "TV",
]

transition_matrix = np.array([
    [0.2, 0.3, 0.5],   # Chabudaiから
    [0.3, 0.1, 0.6],   # Husumaから
    [0.0, 0.5, 0.5],   # TVから
])

state_symbol = {
    "Chabudai": "C",
    "Husuma": "H",
    "TV": "T",
}

state_position = {
    "Chabudai": (0.5, 1.0),
    "Husuma": (2.5, 2.5),
    "TV": (2.5, 0.5),
}

state_color = {
    "Chabudai": "tab:blue",
    "Husuma": "tab:orange",
    "TV": "tab:green",
}


# =========================================================
# 3. 状態系列を生成
# =========================================================

def generate_sequence(steps, start_position="TV", seed=None):
    if steps < 0:
        raise ValueError("stepsは0以上にしてください。")

    if start_position not in states:
        raise ValueError(
            f"start_positionは{states}のいずれかにしてください。"
        )

    row_sums = transition_matrix.sum(axis=1)

    if not np.allclose(row_sums, 1.0):
        raise ValueError(
            "遷移確率行列の各行の合計は1である必要があります。"
        )

    rng = np.random.default_rng(seed)

    current_position = start_position
    sequence = [current_position]

    for _ in range(steps):
        current_index = states.index(current_position)

        current_position = rng.choice(
            states,
            p=transition_matrix[current_index],
        )

        sequence.append(current_position)

    return sequence


# =========================================================
# 4. GUIアプリケーション
# =========================================================

class MarkovAnimationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Markov Chain Animation")
        self.root.geometry("980x820")
        self.root.minsize(850, 700)

        self.state_history = generate_sequence(
            steps=STEPS,
            start_position=START_POSITION,
            seed=SEED,
        )

        self.current_frame = 0
        self.running = False
        self.after_id = None
        self.interval = INITIAL_INTERVAL

        self.create_widgets()
        self.create_plot()
        self.update_frame(0)

        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

    # -----------------------------------------------------
    # GUI部品
    # -----------------------------------------------------

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=8)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.plot_frame = ttk.Frame(main_frame)
        self.plot_frame.pack(fill=tk.BOTH, expand=True)

        control_frame = ttk.Frame(main_frame, padding=(0, 8, 0, 0))
        control_frame.pack(fill=tk.X)

        self.start_button = ttk.Button(
            control_frame,
            text="開始",
            command=self.start_animation,
        )
        self.start_button.pack(side=tk.LEFT, padx=4)

        self.pause_button = ttk.Button(
            control_frame,
            text="一時停止",
            command=self.pause_animation,
        )
        self.pause_button.pack(side=tk.LEFT, padx=4)

        self.step_button = ttk.Button(
            control_frame,
            text="1ステップ",
            command=self.step_animation,
        )
        self.step_button.pack(side=tk.LEFT, padx=4)

        self.reset_button = ttk.Button(
            control_frame,
            text="リセット",
            command=self.reset_animation,
        )
        self.reset_button.pack(side=tk.LEFT, padx=4)

        self.regenerate_button = ttk.Button(
            control_frame,
            text="系列再生成",
            command=self.regenerate_sequence,
        )
        self.regenerate_button.pack(side=tk.LEFT, padx=4)

        ttk.Label(
            control_frame,
            text="速度",
        ).pack(side=tk.LEFT, padx=(20, 4))

        self.speed_var = tk.DoubleVar(value=5.0)

        self.speed_scale = ttk.Scale(
            control_frame,
            from_=1,
            to=20,
            orient=tk.HORIZONTAL,
            variable=self.speed_var,
            command=self.change_speed,
            length=180,
        )
        self.speed_scale.pack(side=tk.LEFT, padx=4)

        self.speed_label = ttk.Label(
            control_frame,
            text="5.0倍",
            width=8,
        )
        self.speed_label.pack(side=tk.LEFT, padx=4)

        self.exit_button = ttk.Button(
            control_frame,
            text="終了",
            command=self.close_app,
        )
        self.exit_button.pack(side=tk.RIGHT, padx=4)

        status_frame = ttk.Frame(main_frame, padding=(0, 8, 0, 0))
        status_frame.pack(fill=tk.X)

        self.status_var = tk.StringVar(value="停止中")

        ttk.Label(
            status_frame,
            textvariable=self.status_var,
        ).pack(side=tk.LEFT)

        self.progress_var = tk.DoubleVar(value=0)

        self.progress_bar = ttk.Progressbar(
            status_frame,
            variable=self.progress_var,
            maximum=len(self.state_history) - 1,
        )
        self.progress_bar.pack(
            side=tk.LEFT,
            fill=tk.X,
            expand=True,
            padx=(12, 0),
        )

    # -----------------------------------------------------
    # グラフ作成
    # -----------------------------------------------------

    def create_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(8, 7))

        self.ax.set_xlim(0, 3)
        self.ax.set_ylim(0, 3)
        self.ax.set_aspect("equal")
        self.ax.set_xticks([])
        self.ax.set_yticks([])

        self.ax.set_title(
            "Markov Chain State Animation",
            fontsize=16,
            pad=20,
        )

        self.state_circles = {}

        for state, position in state_position.items():
            x, y = position

            circle = plt.Circle(
                (x, y),
                radius=0.32,
                facecolor="white",
                edgecolor=state_color[state],
                linewidth=3,
                alpha=0.9,
            )

            self.ax.add_patch(circle)
            self.state_circles[state] = circle

            self.ax.text(
                x,
                y,
                state,
                fontsize=12,
                ha="center",
                va="center",
            )

        self.draw_all_arrows()

        self.ax.text(
            0.05,
            2.95,
            "C → C : 0.2",
            fontsize=9,
            ha="left",
            va="top",
        )

        self.ax.text(
            1.95,
            2.95,
            "H → H : 0.1",
            fontsize=9,
            ha="left",
            va="top",
        )

        self.ax.text(
            1.95,
            0.05,
            "T → T : 0.5",
            fontsize=9,
            ha="left",
            va="bottom",
        )

        self.marker, = self.ax.plot(
            [],
            [],
            marker="o",
            markersize=20,
            linestyle="None",
            markeredgecolor="black",
            markeredgewidth=1.5,
            zorder=10,
        )

        self.current_state_text = self.ax.text(
            1.5,
            2.82,
            "",
            fontsize=14,
            ha="center",
            va="center",
        )

        self.step_text = self.ax.text(
            1.5,
            0.16,
            "",
            fontsize=12,
            ha="center",
            va="center",
        )

        self.history_text = self.ax.text(
            0.06,
            2.72,
            "",
            fontsize=9,
            ha="left",
            va="top",
            family="monospace",
        )

        self.rate_text = self.ax.text(
            0.06,
            0.05,
            "",
            fontsize=9,
            ha="left",
            va="bottom",
            family="monospace",
        )

        self.canvas = FigureCanvasTkAgg(
            self.fig,
            master=self.plot_frame,
        )

        self.canvas.draw()

        self.canvas.get_tk_widget().pack(
            fill=tk.BOTH,
            expand=True,
        )

    def draw_transition_arrow(
        self,
        start_state,
        end_state,
        probability,
        curve=0.0,
        label_offset=(0.0, 0.0),
    ):
        x1, y1 = state_position[start_state]
        x2, y2 = state_position[end_state]

        self.ax.annotate(
            "",
            xy=(x2, y2),
            xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle="->",
                linewidth=1.5,
                alpha=0.45,
                shrinkA=28,
                shrinkB=28,
                connectionstyle=f"arc3,rad={curve}",
            ),
        )

        middle_x = (x1 + x2) / 2 + label_offset[0]
        middle_y = (y1 + y2) / 2 + label_offset[1]

        self.ax.text(
            middle_x,
            middle_y,
            f"{probability:.1f}",
            fontsize=10,
            ha="center",
            va="center",
            bbox=dict(
                boxstyle="round,pad=0.15",
                facecolor="white",
                alpha=0.8,
                edgecolor="none",
            ),
        )

    def draw_all_arrows(self):
        self.draw_transition_arrow(
            "Chabudai", "Husuma", 0.3,
            curve=0.18,
            label_offset=(-0.15, 0.12),
        )

        self.draw_transition_arrow(
            "Husuma", "Chabudai", 0.3,
            curve=0.18,
            label_offset=(0.15, -0.12),
        )

        self.draw_transition_arrow(
            "Chabudai", "TV", 0.5,
            curve=-0.18,
            label_offset=(-0.05, -0.15),
        )

        self.draw_transition_arrow(
            "TV", "Chabudai", 0.0,
            curve=-0.18,
            label_offset=(0.05, 0.15),
        )

        self.draw_transition_arrow(
            "Husuma", "TV", 0.6,
            curve=0.18,
            label_offset=(-0.15, 0.0),
        )

        self.draw_transition_arrow(
            "TV", "Husuma", 0.5,
            curve=0.18,
            label_offset=(0.15, 0.0),
        )

    # -----------------------------------------------------
    # フレーム更新
    # -----------------------------------------------------

    def update_frame(self, frame):
        frame = max(0, min(frame, len(self.state_history) - 1))
        self.current_frame = frame

        current_state = self.state_history[frame]
        x, y = state_position[current_state]

        self.marker.set_data([x], [y])
        self.marker.set_markerfacecolor(
            state_color[current_state]
        )

        self.current_state_text.set_text(
            f"Current state: {current_state}"
        )

        self.step_text.set_text(
            f"Step: {frame} / {len(self.state_history) - 1}"
        )

        history_symbols = "".join(
            state_symbol[state]
            for state in self.state_history[:frame + 1]
        )

        self.history_text.set_text(
            "History:\n" + history_symbols[-60:]
        )

        partial_history = self.state_history[:frame + 1]
        partial_total = len(partial_history)

        rates = {
            state: partial_history.count(state) / partial_total * 100
            for state in states
        }

        self.rate_text.set_text(
            "Occupancy rate\n"
            f"C: {rates['Chabudai']:6.2f}%\n"
            f"H: {rates['Husuma']:6.2f}%\n"
            f"T: {rates['TV']:6.2f}%"
        )

        for state in states:
            if state == current_state:
                self.state_circles[state].set_facecolor(
                    state_color[state]
                )
                self.state_circles[state].set_alpha(0.35)
            else:
                self.state_circles[state].set_facecolor("white")
                self.state_circles[state].set_alpha(0.9)

        self.progress_var.set(frame)
        self.canvas.draw_idle()

    # -----------------------------------------------------
    # ボタン操作
    # -----------------------------------------------------

    def start_animation(self):
        if self.running:
            return

        if self.current_frame >= len(self.state_history) - 1:
            self.current_frame = 0
            self.update_frame(0)

        self.running = True
        self.status_var.set("再生中")
        self.schedule_next_frame()

    def pause_animation(self):
        self.running = False
        self.status_var.set("一時停止")

        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

    def step_animation(self):
        self.pause_animation()

        if self.current_frame < len(self.state_history) - 1:
            self.update_frame(self.current_frame + 1)
        else:
            self.status_var.set("最終ステップです")

    def reset_animation(self):
        self.pause_animation()
        self.current_frame = 0
        self.update_frame(0)
        self.status_var.set("リセットしました")

    def regenerate_sequence(self):
        self.pause_animation()

        new_seed = np.random.SeedSequence().entropy

        self.state_history = generate_sequence(
            steps=STEPS,
            start_position=START_POSITION,
            seed=new_seed,
        )

        self.progress_bar.configure(
            maximum=len(self.state_history) - 1
        )

        self.current_frame = 0
        self.update_frame(0)
        self.status_var.set("新しい状態系列を生成しました")

    def change_speed(self, _value=None):
        speed = max(1.0, self.speed_var.get())

        self.interval = max(
            10,
            int(1000 / speed),
        )

        self.speed_label.configure(
            text=f"{speed:.1f}倍"
        )

    def schedule_next_frame(self):
        if not self.running:
            return

        if self.current_frame >= len(self.state_history) - 1:
            self.running = False
            self.status_var.set("終了")
            self.after_id = None
            return

        self.update_frame(self.current_frame + 1)

        self.after_id = self.root.after(
            self.interval,
            self.schedule_next_frame,
        )

    def close_app(self):
        self.pause_animation()
        plt.close(self.fig)
        self.root.destroy()


# =========================================================
# 5. 実行
# =========================================================

def main():
    root = tk.Tk()

    try:
        app = MarkovAnimationApp(root)
        root.mainloop()

    except Exception as exc:
        messagebox.showerror(
            "エラー",
            str(exc),
        )
        raise


if __name__ == "__main__":
    main()
