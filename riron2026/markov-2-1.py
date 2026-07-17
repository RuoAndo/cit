# Jupyter Notebookの場合は、先に別セルで実行
# %matplotlib qt

import numpy as np
import matplotlib.pyplot as plt

from matplotlib import animation
from matplotlib.widgets import Button


# =========================================================
# 1. マルコフ連鎖の設定
# =========================================================

states = ["Chabudai", "Husuma", "TV"]

# 行：現在の状態
# 列：次の状態
transition_matrix = np.array([
    [0.2, 0.3, 0.5],   # Chabudaiから
    [0.3, 0.1, 0.6],   # Husumaから
    [0.0, 0.5, 0.5]    # TVから
])


state_symbol = {
    "Chabudai": "C",
    "Husuma": "H",
    "TV": "T"
}


state_position = {
    "Chabudai": (0.5, 1.0),
    "Husuma": (2.5, 2.5),
    "TV": (2.5, 0.5)
}


# =========================================================
# 2. 状態系列を生成する関数
# =========================================================

def generate_sequence(steps, start_position="TV", seed=None):
    """
    遷移確率行列に従って状態系列を生成する。
    """

    rng = np.random.default_rng(seed)

    current_position = start_position
    sequence = [current_position]

    for _ in range(steps):

        current_index = states.index(current_position)

        current_position = rng.choice(
            states,
            p=transition_matrix[current_index]
        )

        sequence.append(current_position)

    return sequence


# =========================================================
# 3. 状態系列の生成
# =========================================================

STEPS = 50
START_POSITION = "TV"
SEED = 10

state_history = generate_sequence(
    steps=STEPS,
    start_position=START_POSITION,
    seed=SEED
)

print("生成された状態系列")
print(state_history)

state_string = "".join(
    state_symbol[state]
    for state in state_history
)

print()
print("記号による状態系列")
print(state_string)


# =========================================================
# 4. 描画領域の作成
# =========================================================

fig, ax = plt.subplots(figsize=(8, 8))

# 下側にボタンを置くための余白
plt.subplots_adjust(bottom=0.18)

try:
    fig.canvas.manager.set_window_title(
        "Markov Chain Animation"
    )
except Exception:
    pass


ax.set_xlim(0, 3)
ax.set_ylim(0, 3)
ax.set_aspect("equal")

ax.set_xticks([])
ax.set_yticks([])

ax.set_title(
    "Markov Chain State Animation",
    fontsize=16
)


# =========================================================
# 5. 状態を表す円
# =========================================================

for state, (x, y) in state_position.items():

    circle = plt.Circle(
        (x, y),
        0.30,
        fill=False,
        linewidth=2
    )

    ax.add_patch(circle)

    ax.text(
        x,
        y,
        state,
        fontsize=13,
        ha="center",
        va="center"
    )


# =========================================================
# 6. 状態間の矢印
# =========================================================

def draw_arrow(start_state, end_state, probability, curve=0.0):
    """
    状態間の遷移矢印を描画する。
    """

    x1, y1 = state_position[start_state]
    x2, y2 = state_position[end_state]

    ax.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops=dict(
            arrowstyle="->",
            linewidth=1,
            alpha=0.45,
            connectionstyle=f"arc3,rad={curve}",
            shrinkA=25,
            shrinkB=25
        )
    )

    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2

    ax.text(
        mx,
        my,
        f"{probability:.1f}",
        fontsize=10,
        ha="center",
        va="center",
        bbox=dict(
            facecolor="white",
            edgecolor="none",
            alpha=0.8
        )
    )


draw_arrow("Chabudai", "Husuma", 0.3, curve=0.15)
draw_arrow("Husuma", "Chabudai", 0.3, curve=0.15)

draw_arrow("Chabudai", "TV", 0.5, curve=-0.15)
draw_arrow("TV", "Chabudai", 0.0, curve=-0.15)

draw_arrow("Husuma", "TV", 0.6, curve=0.15)
draw_arrow("TV", "Husuma", 0.5, curve=0.15)


# =========================================================
# 7. 自己遷移確率
# =========================================================

self_loop_positions = {
    "Chabudai": (0.32, 1.48),
    "Husuma": (2.48, 2.96),
    "TV": (2.62, 0.08)
}

for i, state in enumerate(states):

    x, y = self_loop_positions[state]

    ax.text(
        x,
        y,
        f"{state} -> {state}: "
        f"{transition_matrix[i, i]:.1f}",
        fontsize=9,
        ha="center"
    )


# =========================================================
# 8. 移動するマーカー
# =========================================================

marker, = ax.plot(
    [],
    [],
    marker="o",
    markersize=25,
    linestyle="None",
    zorder=10
)


state_text = ax.text(
    1.5,
    2.85,
    "",
    fontsize=14,
    ha="center"
)


step_text = ax.text(
    1.5,
    0.18,
    "",
    fontsize=12,
    ha="center"
)


history_text = ax.text(
    0.05,
    2.75,
    "",
    fontsize=10,
    ha="left",
    va="top"
)


# =========================================================
# 9. アニメーション制御用変数
# =========================================================

current_frame = 0
is_running = False


# =========================================================
# 10. 指定したフレームを描画
# =========================================================

def draw_frame(frame):
    """
    指定されたフレームを画面に描画する。
    """

    global current_frame

    current_frame = int(frame)

    current_state = state_history[current_frame]

    x, y = state_position[current_state]

    marker.set_data([x], [y])

    state_text.set_text(
        f"Current state: {current_state}"
    )

    step_text.set_text(
        f"Step: {current_frame} / "
        f"{len(state_history) - 1}"
    )

    history_symbols = "".join(
        state_symbol[state]
        for state in state_history[:current_frame + 1]
    )

    history_text.set_text(
        "History: " + history_symbols[-30:]
    )

    fig.canvas.draw_idle()


# =========================================================
# 11. 初期化関数
# =========================================================

def init():

    draw_frame(0)

    return marker, state_text, step_text, history_text


# =========================================================
# 12. アニメーション関数
# =========================================================

def animate(_):
    """
    タイマーが動くたびに1ステップ進める。
    """

    global current_frame
    global is_running

    if not is_running:
        return marker, state_text, step_text, history_text

    if current_frame < len(state_history) - 1:
        current_frame += 1
        draw_frame(current_frame)

    else:
        # 最後まで到達したら停止
        is_running = False
        anim.event_source.stop()

    return marker, state_text, step_text, history_text


# =========================================================
# 13. ボタン処理
# =========================================================

def play_animation(event):
    """
    再生ボタン
    """

    global is_running
    global current_frame

    # 最後まで進んでいた場合は最初へ戻す
    if current_frame >= len(state_history) - 1:
        current_frame = 0
        draw_frame(current_frame)

    is_running = True
    anim.event_source.start()


def pause_animation(event):
    """
    一時停止ボタン
    """

    global is_running

    is_running = False
    anim.event_source.stop()


def next_step(event):
    """
    1ステップ進むボタン
    """

    global current_frame
    global is_running

    is_running = False
    anim.event_source.stop()

    if current_frame < len(state_history) - 1:
        current_frame += 1

    draw_frame(current_frame)


def previous_step(event):
    """
    1ステップ戻るボタン
    """

    global current_frame
    global is_running

    is_running = False
    anim.event_source.stop()

    if current_frame > 0:
        current_frame -= 1

    draw_frame(current_frame)


def restart_animation(event):
    """
    最初に戻るボタン
    """

    global current_frame
    global is_running

    is_running = False
    anim.event_source.stop()

    current_frame = 0
    draw_frame(current_frame)


def regenerate_sequence(event):
    """
    新しい状態系列を生成するボタン
    """

    global state_history
    global current_frame
    global is_running

    is_running = False
    anim.event_source.stop()

    # シードを指定しないことで毎回異なる系列にする
    state_history = generate_sequence(
        steps=STEPS,
        start_position=START_POSITION,
        seed=None
    )

    current_frame = 0
    draw_frame(current_frame)

    print()
    print("新しい状態系列")
    print(state_history)


# =========================================================
# 14. ボタン配置
# =========================================================

# left, bottom, width, height
ax_restart = plt.axes([0.07, 0.05, 0.12, 0.055])
ax_previous = plt.axes([0.21, 0.05, 0.12, 0.055])
ax_play = plt.axes([0.35, 0.05, 0.12, 0.055])
ax_pause = plt.axes([0.49, 0.05, 0.12, 0.055])
ax_next = plt.axes([0.63, 0.05, 0.12, 0.055])
ax_new = plt.axes([0.77, 0.05, 0.16, 0.055])


button_restart = Button(
    ax_restart,
    "Restart"
)

button_previous = Button(
    ax_previous,
    "Previous"
)

button_play = Button(
    ax_play,
    "Play"
)

button_pause = Button(
    ax_pause,
    "Pause"
)

button_next = Button(
    ax_next,
    "Next"
)

button_new = Button(
    ax_new,
    "New Sequence"
)


# ボタンと処理を接続
button_restart.on_clicked(restart_animation)
button_previous.on_clicked(previous_step)
button_play.on_clicked(play_animation)
button_pause.on_clicked(pause_animation)
button_next.on_clicked(next_step)
button_new.on_clicked(regenerate_sequence)


# =========================================================
# 15. アニメーション作成
# =========================================================

anim = animation.FuncAnimation(
    fig,
    animate,
    init_func=init,
    frames=None,
    interval=500,
    repeat=True,
    blit=False,
    cache_frame_data=False
)


# 最初は停止状態
anim.event_source.stop()

# 初期状態を表示
draw_frame(0)


# =========================================================
# 16. ウィンドウ表示
# =========================================================

plt.show()