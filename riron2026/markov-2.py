# Jupyter Notebookで実行する場合は、最初にこの行を実行
# %matplotlib qt

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation


# =========================================================
# 1. マルコフ連鎖の設定
# =========================================================

states = ["Chabudai", "Husuma", "TV"]

# 行：現在の状態
# 列：次の状態
#
#              C     H     T
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

fig, ax = plt.subplots(figsize=(7, 7))

# ウィンドウタイトル
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
# 7. 自己遷移確率の表示
# =========================================================

self_loop_positions = {
    "Chabudai": (0.22, 1.42),
    "Husuma": (2.55, 2.96),
    "TV": (2.82, 0.18)
}

for i, state in enumerate(states):

    x, y = self_loop_positions[state]

    ax.text(
        x,
        y,
        f"{state} → {state}: "
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
    2.9,
    "",
    fontsize=14,
    ha="center"
)


step_text = ax.text(
    1.5,
    0.08,
    "",
    fontsize=12,
    ha="center"
)


history_text = ax.text(
    0.05,
    2.78,
    "",
    fontsize=10,
    ha="left",
    va="top"
)


# =========================================================
# 9. 初期化関数
# =========================================================

def init():

    marker.set_data([], [])

    state_text.set_text("")
    step_text.set_text("")
    history_text.set_text("")

    return marker, state_text, step_text, history_text


# =========================================================
# 10. アニメーション関数
# =========================================================

def animate(frame):

    current_state = state_history[frame]

    x, y = state_position[current_state]

    marker.set_data([x], [y])

    state_text.set_text(
        f"Current state: {current_state}"
    )

    step_text.set_text(
        f"Step: {frame} / {len(state_history) - 1}"
    )

    history_symbols = "".join(
        state_symbol[state]
        for state in state_history[:frame + 1]
    )

    history_text.set_text(
        "History: " + history_symbols[-30:]
    )

    return marker, state_text, step_text, history_text


# =========================================================
# 11. アニメーション作成
# =========================================================

anim = animation.FuncAnimation(
    fig,
    animate,
    init_func=init,
    frames=len(state_history),
    interval=500,
    repeat=False,
    blit=False
)


# =========================================================
# 12. 別ウィンドウで表示
# =========================================================

plt.tight_layout()
plt.show()