import tkinter as tk
from tkinter import ttk, messagebox

import numpy as np
import matplotlib

# Tkinterウィンドウ内にMatplotlibを表示
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)


# =========================================================
# 1. マルコフ連鎖の設定
# =========================================================

STATES = [
    "Chabudai",
    "Husuma",
    "TV"
]

STATE_SYMBOL = {
    "Chabudai": "C",
    "Husuma": "H",
    "TV": "T"
}

STATE_POSITION = {
    "Chabudai": (0.5, 1.0),
    "Husuma": (2.5, 2.5),
    "TV": (2.5, 0.5)
}

STATE_COLOR = {
    "Chabudai": "tab:blue",
    "Husuma": "tab:orange",
    "TV": "tab:green"
}


# 行：現在の状態
# 列：次の状態
#
#                 C     H     T
TRANSITION_MATRIX = np.array([
    [0.2, 0.3, 0.5],   # Chabudaiから
    [0.3, 0.1, 0.6],   # Husumaから
    [0.0, 0.5, 0.5]    # TVから
], dtype=float)


# =========================================================
# 2. マルコフ連鎖の関数
# =========================================================

def validate_transition_matrix(matrix):
    """
    遷移確率行列を検査する。
    """

    if matrix.shape != (len(STATES), len(STATES)):
        raise ValueError(
            "遷移確率行列の大きさが状態数と一致していません。"
        )

    if np.any(matrix < 0):
        raise ValueError(
            "遷移確率に負の値は指定できません。"
        )

    if not np.allclose(matrix.sum(axis=1), 1.0):
        raise ValueError(
            "遷移確率行列の各行の合計は1である必要があります。"
        )


def calculate_stationary_distribution(matrix):
    """
    πP = πを満たす定常分布を計算する。
    """

    eigenvalues, eigenvectors = np.linalg.eig(matrix.T)

    index = np.argmin(
        np.abs(eigenvalues - 1.0)
    )

    stationary = np.real(
        eigenvectors[:, index]
    )

    if stationary.sum() < 0:
        stationary = -stationary

    stationary = stationary / stationary.sum()

    return stationary


validate_transition_matrix(
    TRANSITION_MATRIX
)

STATIONARY_DISTRIBUTION = (
    calculate_stationary_distribution(
        TRANSITION_MATRIX
    )
)

STATIONARY_RATES = {
    state: STATIONARY_DISTRIBUTION[i] * 100
    for i, state in enumerate(STATES)
}


# =========================================================
# 3. アプリケーションクラス
# =========================================================

class MarkovAnimationApp:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Markov Chain Animation"
        )

        self.root.geometry(
            "1400x850"
        )

        self.root.minsize(
            1000,
            650
        )

        # ---------------------------------------------
        # 動作状態
        # ---------------------------------------------

        self.running = False

        self.current_step = 0

        self.current_state = "TV"

        self.after_id = None

        self.rng = np.random.default_rng(10)

        self.state_history = [
            self.current_state
        ]

        self.cumulative_rates = {
            state: []
            for state in STATES
        }

        self.state_counts = {
            state: 0
            for state in STATES
        }

        # 初期状態をカウント
        self.state_counts[
            self.current_state
        ] = 1

        self.update_cumulative_rates()

        # ---------------------------------------------
        # Tkinter変数
        # ---------------------------------------------

        self.start_state_var = tk.StringVar(
            value="TV"
        )

        self.seed_var = tk.StringVar(
            value="10"
        )

        self.max_steps_var = tk.StringVar(
            value="500"
        )

        self.speed_var = tk.IntVar(
            value=50
        )

        self.speed_text_var = tk.StringVar(
            value="50 ms"
        )

        self.status_var = tk.StringVar(
            value="停止中"
        )

        self.current_state_var = tk.StringVar(
            value="現在状態: TV"
        )

        self.current_step_var = tk.StringVar(
            value="ステップ: 0 / 500"
        )

        self.rate_var = tk.StringVar(
            value=""
        )

        # ---------------------------------------------
        # 画面作成
        # ---------------------------------------------

        self.create_control_panel()

        self.create_figure()

        self.create_navigation_toolbar()

        self.update_rate_label()

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close_window
        )


    # =====================================================
    # 4. 操作パネル
    # =====================================================

    def create_control_panel(self):

        control_frame = ttk.Frame(
            self.root,
            padding=8
        )

        control_frame.pack(
            side=tk.TOP,
            fill=tk.X
        )

        # ---------------------------------------------
        # 開始状態
        # ---------------------------------------------

        ttk.Label(
            control_frame,
            text="開始状態"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=4
        )

        start_state_combo = ttk.Combobox(
            control_frame,
            textvariable=self.start_state_var,
            values=STATES,
            state="readonly",
            width=12
        )

        start_state_combo.grid(
            row=0,
            column=1,
            padx=5,
            pady=4
        )

        # ---------------------------------------------
        # 乱数シード
        # ---------------------------------------------

        ttk.Label(
            control_frame,
            text="乱数シード"
        ).grid(
            row=0,
            column=2,
            padx=5,
            pady=4
        )

        seed_entry = ttk.Entry(
            control_frame,
            textvariable=self.seed_var,
            width=8
        )

        seed_entry.grid(
            row=0,
            column=3,
            padx=5,
            pady=4
        )

        # ---------------------------------------------
        # 最大ステップ数
        # ---------------------------------------------

        ttk.Label(
            control_frame,
            text="最大ステップ"
        ).grid(
            row=0,
            column=4,
            padx=5,
            pady=4
        )

        max_steps_entry = ttk.Entry(
            control_frame,
            textvariable=self.max_steps_var,
            width=8
        )

        max_steps_entry.grid(
            row=0,
            column=5,
            padx=5,
            pady=4
        )

        # ---------------------------------------------
        # ボタン
        # ---------------------------------------------

        self.start_button = ttk.Button(
            control_frame,
            text="開始",
            command=self.start_animation
        )

        self.start_button.grid(
            row=0,
            column=6,
            padx=5,
            pady=4
        )

        self.pause_button = ttk.Button(
            control_frame,
            text="一時停止",
            command=self.pause_animation
        )

        self.pause_button.grid(
            row=0,
            column=7,
            padx=5,
            pady=4
        )

        self.step_button = ttk.Button(
            control_frame,
            text="1ステップ",
            command=self.one_step
        )

        self.step_button.grid(
            row=0,
            column=8,
            padx=5,
            pady=4
        )

        self.reset_button = ttk.Button(
            control_frame,
            text="リセット",
            command=self.reset_animation
        )

        self.reset_button.grid(
            row=0,
            column=9,
            padx=5,
            pady=4
        )

        self.regenerate_button = ttk.Button(
            control_frame,
            text="再生成",
            command=self.regenerate_animation
        )

        self.regenerate_button.grid(
            row=0,
            column=10,
            padx=5,
            pady=4
        )

        # ---------------------------------------------
        # 速度スライダー
        # ---------------------------------------------

        ttk.Label(
            control_frame,
            text="速度"
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=4
        )

        # 小さい値ほど高速
        speed_scale = ttk.Scale(
            control_frame,
            from_=10,
            to=1000,
            orient=tk.HORIZONTAL,
            variable=self.speed_var,
            command=self.change_speed,
            length=300
        )

        speed_scale.grid(
            row=1,
            column=1,
            columnspan=4,
            padx=5,
            pady=4,
            sticky="ew"
        )

        ttk.Label(
            control_frame,
            textvariable=self.speed_text_var,
            width=10
        ).grid(
            row=1,
            column=5,
            padx=5,
            pady=4
        )

        ttk.Label(
            control_frame,
            text="小さい値ほど高速"
        ).grid(
            row=1,
            column=6,
            columnspan=2,
            padx=5,
            pady=4
        )

        # ---------------------------------------------
        # 状態表示
        # ---------------------------------------------

        ttk.Label(
            control_frame,
            textvariable=self.status_var
        ).grid(
            row=1,
            column=8,
            padx=5,
            pady=4
        )

        ttk.Label(
            control_frame,
            textvariable=self.current_state_var
        ).grid(
            row=1,
            column=9,
            padx=5,
            pady=4
        )

        ttk.Label(
            control_frame,
            textvariable=self.current_step_var
        ).grid(
            row=1,
            column=10,
            padx=5,
            pady=4
        )


    # =====================================================
    # 5. Matplotlib描画領域
    # =====================================================

    def create_figure(self):

        self.figure, (
            self.ax_state,
            self.ax_probability
        ) = plt.subplots(
            1,
            2,
            figsize=(14, 7)
        )

        self.figure.suptitle(
            "Markov Chain Animation and Stationary Probability",
            fontsize=16
        )

        self.figure.subplots_adjust(
            left=0.05,
            right=0.97,
            bottom=0.12,
            top=0.90,
            wspace=0.25
        )

        self.setup_state_plot()

        self.setup_probability_plot()

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=self.root
        )

        self.canvas.draw()

        self.canvas.get_tk_widget().pack(
            side=tk.TOP,
            fill=tk.BOTH,
            expand=True
        )

        # ウィンドウ下部の数値表示
        rate_frame = ttk.Frame(
            self.root,
            padding=5
        )

        rate_frame.pack(
            side=tk.BOTTOM,
            fill=tk.X
        )

        ttk.Label(
            rate_frame,
            textvariable=self.rate_var,
            font=("Consolas", 11)
        ).pack(
            side=tk.LEFT,
            padx=10
        )


    # =====================================================
    # 6. 左側の状態遷移図
    # =====================================================

    def setup_state_plot(self):

        ax = self.ax_state

        ax.clear()

        ax.set_xlim(
            0,
            3
        )

        ax.set_ylim(
            0,
            3
        )

        ax.set_aspect(
            "equal"
        )

        ax.set_xticks([])
        ax.set_yticks([])

        ax.set_title(
            "State transition"
        )

        self.state_circles = {}

        for state, (x, y) in STATE_POSITION.items():

            circle = plt.Circle(
                (x, y),
                radius=0.32,
                facecolor="white",
                edgecolor=STATE_COLOR[state],
                linewidth=3
            )

            ax.add_patch(circle)

            self.state_circles[state] = circle

            ax.text(
                x,
                y,
                state,
                fontsize=12,
                ha="center",
                va="center"
            )

        # 遷移矢印
        self.draw_transition_arrow(
            "Chabudai",
            "Husuma",
            TRANSITION_MATRIX[0, 1],
            curve=0.18,
            label_offset=(-0.15, 0.12)
        )

        self.draw_transition_arrow(
            "Husuma",
            "Chabudai",
            TRANSITION_MATRIX[1, 0],
            curve=0.18,
            label_offset=(0.15, -0.12)
        )

        self.draw_transition_arrow(
            "Chabudai",
            "TV",
            TRANSITION_MATRIX[0, 2],
            curve=-0.18,
            label_offset=(-0.05, -0.15)
        )

        self.draw_transition_arrow(
            "TV",
            "Chabudai",
            TRANSITION_MATRIX[2, 0],
            curve=-0.18,
            label_offset=(0.05, 0.15)
        )

        self.draw_transition_arrow(
            "Husuma",
            "TV",
            TRANSITION_MATRIX[1, 2],
            curve=0.18,
            label_offset=(-0.15, 0.0)
        )

        self.draw_transition_arrow(
            "TV",
            "Husuma",
            TRANSITION_MATRIX[2, 1],
            curve=0.18,
            label_offset=(0.15, 0.0)
        )

        # 自己遷移
        ax.text(
            0.05,
            2.95,
            f"C → C : {TRANSITION_MATRIX[0, 0]:.1f}",
            fontsize=9,
            ha="left",
            va="top"
        )

        ax.text(
            1.90,
            2.95,
            f"H → H : {TRANSITION_MATRIX[1, 1]:.1f}",
            fontsize=9,
            ha="left",
            va="top"
        )

        ax.text(
            1.90,
            0.05,
            f"T → T : {TRANSITION_MATRIX[2, 2]:.1f}",
            fontsize=9,
            ha="left",
            va="bottom"
        )

        self.marker, = ax.plot(
            [],
            [],
            marker="o",
            markersize=22,
            linestyle="None",
            markeredgecolor="black",
            markeredgewidth=1.5,
            zorder=10
        )

        self.history_text = ax.text(
            0.05,
            2.72,
            "",
            fontsize=9,
            ha="left",
            va="top",
            family="monospace"
        )

        self.update_state_plot()


    def draw_transition_arrow(
        self,
        start_state,
        end_state,
        probability,
        curve=0.0,
        label_offset=(0.0, 0.0)
    ):

        x1, y1 = STATE_POSITION[start_state]
        x2, y2 = STATE_POSITION[end_state]

        self.ax_state.annotate(
            "",
            xy=(x2, y2),
            xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle="->",
                linewidth=1.5,
                alpha=0.45,
                shrinkA=28,
                shrinkB=28,
                connectionstyle=f"arc3,rad={curve}"
            )
        )

        middle_x = (
            (x1 + x2) / 2
            + label_offset[0]
        )

        middle_y = (
            (y1 + y2) / 2
            + label_offset[1]
        )

        self.ax_state.text(
            middle_x,
            middle_y,
            f"{probability:.1f}",
            fontsize=10,
            ha="center",
            va="center",
            bbox=dict(
                boxstyle="round,pad=0.15",
                facecolor="white",
                alpha=0.85,
                edgecolor="none"
            )
        )


    # =====================================================
    # 7. 右側の定常確率プロット
    # =====================================================

    def setup_probability_plot(self):

        ax = self.ax_probability

        ax.clear()

        ax.set_xlim(
            0,
            self.get_max_steps()
        )

        ax.set_ylim(
            0,
            100
        )

        ax.set_xlabel(
            "Step"
        )

        ax.set_ylabel(
            "Cumulative occupancy rate (%)"
        )

        ax.set_title(
            "Convergence to stationary probabilities"
        )

        ax.grid(
            alpha=0.3
        )

        self.probability_lines = {}

        for state in STATES:

            line, = ax.plot(
                [],
                [],
                linewidth=2,
                label=f"{state} observed",
                color=STATE_COLOR[state]
            )

            self.probability_lines[state] = line

        # 理論上の定常確率
        for state in STATES:

            ax.axhline(
                STATIONARY_RATES[state],
                linestyle="--",
                linewidth=1.5,
                color=STATE_COLOR[state],
                alpha=0.7,
                label=(
                    f"{state} theoretical "
                    f"{STATIONARY_RATES[state]:.2f}%"
                )
            )

        self.current_step_line = ax.axvline(
            0,
            linestyle=":",
            linewidth=1.5,
            alpha=0.7
        )

        self.probability_points = {}

        for state in STATES:

            point, = ax.plot(
                [],
                [],
                marker="o",
                markersize=7,
                linestyle="None",
                color=STATE_COLOR[state]
            )

            self.probability_points[state] = point

        ax.legend(
            loc="upper right",
            fontsize=8,
            ncol=2
        )


    # =====================================================
    # 8. 状態更新
    # =====================================================

    def generate_next_state(self):

        current_index = STATES.index(
            self.current_state
        )

        next_state = self.rng.choice(
            STATES,
            p=TRANSITION_MATRIX[current_index]
        )

        self.current_state = next_state

        self.current_step += 1

        self.state_history.append(
            next_state
        )

        self.state_counts[
            next_state
        ] += 1

        self.update_cumulative_rates()


    def update_cumulative_rates(self):

        total = len(
            self.state_history
        )

        for state in STATES:

            rate = (
                self.state_counts[state]
                / total
                * 100
            )

            self.cumulative_rates[state].append(
                rate
            )


    # =====================================================
    # 9. 描画更新
    # =====================================================

    def update_plots(self):

        self.update_state_plot()

        self.update_probability_plot()

        self.update_rate_label()

        self.canvas.draw_idle()


    def update_state_plot(self):

        x, y = STATE_POSITION[
            self.current_state
        ]

        self.marker.set_data(
            [x],
            [y]
        )

        self.marker.set_markerfacecolor(
            STATE_COLOR[self.current_state]
        )

        for state in STATES:

            circle = self.state_circles[state]

            if state == self.current_state:

                circle.set_facecolor(
                    STATE_COLOR[state]
                )

                circle.set_alpha(
                    0.35
                )

            else:

                circle.set_facecolor(
                    "white"
                )

                circle.set_alpha(
                    1.0
                )

        symbols = "".join(
            STATE_SYMBOL[state]
            for state in self.state_history
        )

        self.history_text.set_text(
            "History:\n"
            + symbols[-70:]
        )

        self.current_state_var.set(
            f"現在状態: {self.current_state}"
        )

        self.current_step_var.set(
            f"ステップ: "
            f"{self.current_step} / "
            f"{self.get_max_steps()}"
        )


    def update_probability_plot(self):

        x_values = np.arange(
            len(self.state_history)
        )

        for state in STATES:

            y_values = np.array(
                self.cumulative_rates[state]
            )

            self.probability_lines[
                state
            ].set_data(
                x_values,
                y_values
            )

            self.probability_points[
                state
            ].set_data(
                [self.current_step],
                [y_values[-1]]
            )

        self.current_step_line.set_xdata(
            [
                self.current_step,
                self.current_step
            ]
        )

        max_steps = self.get_max_steps()

        self.ax_probability.set_xlim(
            0,
            max(
                max_steps,
                10
            )
        )


    def update_rate_label(self):

        total = len(
            self.state_history
        )

        observed_rates = {
            state: (
                self.state_counts[state]
                / total
                * 100
            )
            for state in STATES
        }

        text = (
            f"観測値  "
            f"C: {observed_rates['Chabudai']:6.2f}%  "
            f"H: {observed_rates['Husuma']:6.2f}%  "
            f"T: {observed_rates['TV']:6.2f}%"
            f"    |    "
            f"理論値  "
            f"C: {STATIONARY_RATES['Chabudai']:6.2f}%  "
            f"H: {STATIONARY_RATES['Husuma']:6.2f}%  "
            f"T: {STATIONARY_RATES['TV']:6.2f}%"
        )

        self.rate_var.set(
            text
        )


    # =====================================================
    # 10. ボタン処理
    # =====================================================

    def start_animation(self):

        if self.current_step >= self.get_max_steps():

            messagebox.showinfo(
                "終了",
                "最大ステップに到達しています。"
            )

            return

        if self.running:
            return

        self.running = True

        self.status_var.set(
            "実行中"
        )

        self.run_animation()


    def run_animation(self):

        if not self.running:
            return

        max_steps = self.get_max_steps()

        if self.current_step >= max_steps:

            self.running = False

            self.status_var.set(
                "終了"
            )

            self.after_id = None

            return

        self.generate_next_state()

        self.update_plots()

        interval = max(
            1,
            int(self.speed_var.get())
        )

        self.after_id = self.root.after(
            interval,
            self.run_animation
        )


    def pause_animation(self):

        self.running = False

        self.status_var.set(
            "一時停止"
        )

        if self.after_id is not None:

            self.root.after_cancel(
                self.after_id
            )

            self.after_id = None


    def one_step(self):

        self.pause_animation()

        if self.current_step >= self.get_max_steps():

            messagebox.showinfo(
                "終了",
                "最大ステップに到達しています。"
            )

            return

        self.generate_next_state()

        self.update_plots()

        self.status_var.set(
            "1ステップ実行"
        )


    def reset_animation(self):

        self.pause_animation()

        try:

            seed = int(
                self.seed_var.get()
            )

        except ValueError:

            messagebox.showerror(
                "入力エラー",
                "乱数シードは整数で入力してください。"
            )

            return

        start_state = (
            self.start_state_var.get()
        )

        if start_state not in STATES:

            messagebox.showerror(
                "入力エラー",
                "開始状態が正しくありません。"
            )

            return

        self.rng = np.random.default_rng(
            seed
        )

        self.current_step = 0

        self.current_state = start_state

        self.state_history = [
            start_state
        ]

        self.state_counts = {
            state: 0
            for state in STATES
        }

        self.state_counts[
            start_state
        ] = 1

        self.cumulative_rates = {
            state: []
            for state in STATES
        }

        self.update_cumulative_rates()

        self.setup_probability_plot()

        self.update_plots()

        self.status_var.set(
            "リセット"
        )


    def regenerate_animation(self):

        """
        現在時刻に基づく新しい乱数系列に変更する。
        """

        self.pause_animation()

        new_seed = np.random.SeedSequence().entropy

        new_seed = int(
            new_seed % 1_000_000
        )

        self.seed_var.set(
            str(new_seed)
        )

        self.reset_animation()

        self.status_var.set(
            "新しい系列を生成"
        )


    # =====================================================
    # 11. その他
    # =====================================================

    def change_speed(self, value):

        interval = int(
            float(value)
        )

        self.speed_text_var.set(
            f"{interval} ms"
        )


    def get_max_steps(self):

        try:

            max_steps = int(
                self.max_steps_var.get()
            )

            if max_steps < 1:
                raise ValueError

            return max_steps

        except ValueError:

            return 500


    def create_navigation_toolbar(self):

        toolbar_frame = ttk.Frame(
            self.root
        )

        toolbar_frame.pack(
            side=tk.BOTTOM,
            fill=tk.X
        )

        toolbar = NavigationToolbar2Tk(
            self.canvas,
            toolbar_frame
        )

        toolbar.update()


    def close_window(self):

        self.pause_animation()

        plt.close(
            self.figure
        )

        self.root.destroy()


# =========================================================
# 12. プログラム開始
# =========================================================

def main():

    root = tk.Tk()

    app = MarkovAnimationApp(
        root
    )

    root.mainloop()


if __name__ == "__main__":
    main()