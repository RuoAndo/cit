
2.6 QwKÅÀHðUª
# gp·épbP[WÌé¾
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
# úÊuÅÌÀHÌlq

# }ð`­å«³ÆA}ÌÏ¼ðé¾
fig = plt.figure(figsize=(5, 5))
ax = plt.gca()

# Ô¢Çð`­
plt.plot([1, 1], [0, 1], color='red', linewidth=2)
plt.plot([1, 2], [2, 2], color='red', linewidth=2)
plt.plot([2, 2], [2, 1], color='red', linewidth=2)
plt.plot([2, 3], [1, 1], color='red', linewidth=2)

# óÔð¦·¶S0`S8ð`­
plt.text(0.5, 2.5, 'S0', size=14, ha='center')
plt.text(1.5, 2.5, 'S1', size=14, ha='center')
plt.text(2.5, 2.5, 'S2', size=14, ha='center')
plt.text(0.5, 1.5, 'S3', size=14, ha='center')
plt.text(1.5, 1.5, 'S4', size=14, ha='center')
plt.text(2.5, 1.5, 'S5', size=14, ha='center')
plt.text(0.5, 0.5, 'S6', size=14, ha='center')
plt.text(1.5, 0.5, 'S7', size=14, ha='center')
plt.text(2.5, 0.5, 'S8', size=14, ha='center')
plt.text(0.5, 2.3, 'START', ha='center')
plt.text(2.5, 0.3, 'GOAL', ha='center')

# `æÍÍÌÝèÆÚ·èðÁ·Ýè
ax.set_xlim(0, 3)
ax.set_ylim(0, 3)
plt.tick_params(axis='both', which='both', bottom='off', top='off',
                labelbottom='off', right='off', left='off', labelleft='off')

# »ÝnS0ÉÎÛð`æ·é
line, = ax.plot([0.5], [2.5], marker="o", color='g', markersize=60)
C:\Users\yutar\Anaconda3\envs\rl_env\lib\site-packages\matplotlib\cbook\deprecation.py:107: MatplotlibDeprecationWarning: Passing one of 'on', 'true', 'off', 'false' as a boolean is deprecated; use an actual boolean (True/False) instead.
  warnings.warn(message, mplDeprecation, stacklevel=1)

# úÌûôðè·ép[^theta_0ðÝè

# sÍóÔ0`7AñÍÚ®ûüÅªA¨A«A©ð\·
theta_0 = np.array([[np.nan, 1, 1, np.nan],  # s0
                    [np.nan, 1, np.nan, 1],  # s1
                    [np.nan, np.nan, 1, 1],  # s2
                    [1, 1, 1, np.nan],  # s3
                    [np.nan, np.nan, 1, 1],  # s4
                    [1, np.nan, np.nan, np.nan],  # s5
                    [1, np.nan, np.nan, np.nan],  # s6
                    [1, 1, np.nan, np.nan],  # s7A¦s8ÍS[ÈÌÅAûôÍÈµ
                    ])
# ûôp[^theta_0ð_ûôpiÉÏ··éÖÌè`


def simple_convert_into_pi_from_theta(theta):
    '''PÉðvZ·é'''

    [m, n] = theta.shape  # thetaÌsñTCYðæ¾
    pi = np.zeros((m, n))
    for i in range(0, m):
        pi[i, :] = theta[i, :] / np.nansum(theta[i, :])  # ÌvZ

    pi = np.nan_to_num(pi)  # nanð0ÉÏ·

    return pi

# _s®ûôpi_0ðßé
pi_0 = simple_convert_into_pi_from_theta(theta_0)
# úÌs®¿lÖQðÝè

[a, b] = theta_0.shape  # sÆñÌða, bÉi[
Q = np.random.rand(a, b) * theta_0 * 0.1
# *theta0ð·é±ÆÅvf²ÆÉ|¯ZðµAQÌÇûüÌlªnanÉÈé
# Ã-greedy@ðÀ


def get_action(s, Q, epsilon, pi_0):
    direction = ["up", "right", "down", "left"]

    # s®ðßé
    if np.random.rand() < epsilon:
        # ÃÌm¦Å_É®­
        next_direction = np.random.choice(direction, p=pi_0[s, :])
    else:
        # QÌÅålÌs®ðÌp·é
        next_direction = direction[np.nanargmax(Q[s, :])]

    # s®ðindexÉ
    if next_direction == "up":
        action = 0
    elif next_direction == "right":
        action = 1
    elif next_direction == "down":
        action = 2
    elif next_direction == "left":
        action = 3

    return action


def get_s_next(s, a, Q, epsilon, pi_0):
    direction = ["up", "right", "down", "left"]
    next_direction = direction[a]  # s®aÌûü

    # s®©çÌóÔðßé
    if next_direction == "up":
        s_next = s - 3  # ãÉÚ®·éÆ«ÍóÔÌª3¬³­Èé
    elif next_direction == "right":
        s_next = s + 1  # EÉÚ®·éÆ«ÍóÔÌª1å«­Èé
    elif next_direction == "down":
        s_next = s + 3  # ºÉÚ®·éÆ«ÍóÔÌª3å«­Èé
    elif next_direction == "left":
        s_next = s - 1  # ¶ÉÚ®·éÆ«ÍóÔÌª1¬³­Èé

    return s_next
# QwKÉæés®¿lÖQÌXV


def Q_learning(s, a, r, s_next, Q, eta, gamma):

    if s_next == 8:  # S[µ½ê
        Q[s, a] = Q[s, a] + eta * (r - Q[s, a])

    else:
        Q[s, a] = Q[s, a] + eta * (r + gamma * np.nanmax(Q[s_next,: ]) - Q[s, a])

    return Q
# QwKÅÀHðð­ÖÌè`AóÔÆs®Ìð¨æÑXVµ½QðoÍ


def goal_maze_ret_s_a_Q(Q, epsilon, eta, gamma, pi):
    s = 0  # X^[gn_
    a = a_next = get_action(s, Q, epsilon, pi)  # úÌs®
    s_a_history = [[0, np.nan]]  # G[WFgÌÚ®ðL^·éXg

    while (1):  # S[·éÜÅ[v
        a = a_next  # s®XV

        s_a_history[-1][1] = a
        # »ÝÌóÔiÂÜèêÔÅãÈÌÅindex=-1jÉs®ðãü

        s_next = get_s_next(s, a, Q, epsilon, pi)
        # ÌóÔði[

        s_a_history.append([s_next, np.nan])
        # ÌóÔðãüBs®ÍÜ¾ª©çÈ¢ÌÅnanÉµÄ¨­

        # ñVð^¦,@Ìs®ðßÜ·
        if s_next == 8:
            r = 1  # S[É½Çè¢½ÈçñVð^¦é
            a_next = np.nan
        else:
            r = 0
            a_next = get_action(s_next, Q, epsilon, pi)
            # Ìs®a_nextðßÜ·B

        # ¿lÖðXV
        Q = Q_learning(s, a, r, s_next, Q, eta, gamma)

        # I¹»è
        if s_next == 8:  # S[n_ÈçI¹
            break
        else:
            s = s_next

    return [s_a_history, Q]
# QwKÅÀHðð­

eta = 0.1  # wK¦
gamma = 0.9  # Ôø¦
epsilon = 0.5  # Ã-greedy@Ìúl
v = np.nanmax(Q, axis=1)  # óÔ²ÆÉ¿lÌÅålðßé
is_continue = True
episode = 1

V = []  # Gs\[h²ÆÌóÔ¿lði[·é
V.append(np.nanmax(Q, axis=1))  # óÔ²ÆÉs®¿lÌÅålðßé

while is_continue:  # is_continueªFalseÉÈéÜÅJèÔ·
    print("Gs\[h:" + str(episode))

    # Ã-greedyÌlð­µ¸Â¬³­·é
    epsilon = epsilon / 2

    # QwKÅÀHðð«AÚ®µ½ðÆXVµ½Qðßé
    [s_a_history, Q] = goal_maze_ret_s_a_Q(Q, epsilon, eta, gamma, pi_0)

    # óÔ¿lÌÏ»
    new_v = np.nanmax(Q, axis=1)  # óÔ²ÆÉs®¿lÌÅålðßé
    print(np.sum(np.abs(new_v - v)))  # óÔ¿lÖÌÏ»ðoÍ
    v = new_v
    V.append(v)  # ±ÌGs\[hI¹ÌóÔ¿lÖðÇÁ

    print("ÀHðð­ÌÉ©©Á½XebvÍ" + str(len(s_a_history) - 1) + "Å·")

    # 100Gs\[hJèÔ·
    episode = episode + 1
    if episode > 100:
        break
Gs\[h:1
0.33695783349641584
ÀHðð­ÌÉ©©Á½XebvÍ676Å·
Gs\[h:2
0.09800995966053788
ÀHðð­ÌÉ©©Á½XebvÍ14Å·
Gs\[h:3
0.09791232661824678
ÀHðð­ÌÉ©©Á½XebvÍ18Å·
Gs\[h:4
0.09373145367281005
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:5
0.09250125578394505
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:6
0.09157216378601814
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:7
0.09062211846852089
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:8
0.0896387103252213
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:9
0.08861021709396733
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:10
0.0875262501519074
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:11
0.08637815285133413
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:12
0.08515920972816424
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:13
0.08386471417151692
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:14
0.08249193272840702
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:15
0.08103999643025925
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:16
0.07950974311037037
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:17
0.07790352941437567
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:18
0.07622502690288072
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:19
0.07447901314845165
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:20
0.07267116590403111
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:21
0.07080786615306545
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:22
0.06889601404734899
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:23
0.06694286031601429
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:24
0.06495585462023931
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:25
0.06294251147607507
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:26
0.06091029372453988
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:27
0.05886651305389909
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:28
0.05681824674066879
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:29
0.054772269545764
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:30
0.052734999557598417
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:31
0.05071245669606911
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:32
0.04871023256481488
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:33
0.04673347035141928
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:34
0.04478685351610606
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:35
0.042874602070793466
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:36
0.04100047532554485
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:37
0.039167780063303625
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:38
0.03737938319226247
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:39
0.03563772801512982
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:40
0.0339448533435755
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:41
0.0323024147724445
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:42
0.030711707510698683
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:43
0.02917369024357419
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:44
0.02768900957260012
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:45
0.026258024646585887
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:46
0.024880831657365876
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:47
0.02355728792900269
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:48
0.022287035378472986
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:49
0.021069523169803372
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:50
0.019904029422487923
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:51
0.018789681869120334
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:52
0.017725477386872357
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:53
0.016710300353082963
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:54
0.015742939797159017
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:55
0.014822105339579394
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:56
0.013946441924356234
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:57
0.013114543364184161
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:58
0.012324964727989274
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:59
0.011576233608951214
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:60
0.010866860317587324
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:61
0.01019534704938685
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:62
0.009560196079986483
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:63
0.008959917043182775
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:64
0.008393033348366719
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:65
0.007858087794390012
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:66
0.007353647436583288
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:67
0.006878307762769875
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:68
0.006430696232754052
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:69
0.006009475234031281
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:70
0.005613344504422191
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:71
0.005241043070085549
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:72
0.004891350744940959
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:73
0.0045630892350194685
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:74
0.0042551228886746895
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:75
0.003966359130999408
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:76
0.0036957486181991017
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:77
0.0034422851451395564
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:78
0.003205005336789357
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:79
0.002982988151882915
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:80
0.0027753542248091234
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:81
0.0025812650695137274
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:82
0.0023999221670997217
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:83
0.002230565956815478
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:84
0.0020724747482360195
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:85
0.0019249635706810597
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:86
0.0017873829742647285
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:87
0.0016591177954323744
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:88
0.0015395858984186273
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:89
0.001428236902737745
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:90
0.0013245509056067917
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:91
0.0012280372070851975
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:92
0.00113823304468752
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:93
0.0010547023433052916
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:94
0.0009770344854084234
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:95
0.0009048431057477879
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:96
0.0008377649140651755
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:97
0.0007754585487091958
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:98
0.0007176034634801542
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:99
0.000663898849534772
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
Gs\[h:100
0.0006140625937295363
ÀHðð­ÌÉ©©Á½XebvÍ4Å·
# óÔ¿lÌÏ»ðÂ»µÜ·
# QlURL http://louistiao.me/posts/notebooks/embedding-matplotlib-animations-in-jupyter-notebooks/
from matplotlib import animation
from IPython.display import HTML
import matplotlib.cm as cm  # color map


def init():
    # wiæÌú»
    line.set_data([], [])
    return (line,)


def animate(i):
    # t[²ÆÌ`æàe
    # e}XÉóÔ¿lÌå«³ÉîÃ­Ft«Ìlpð`æ
    line, = ax.plot([0.5], [2.5], marker="s",
                    color=cm.jet(V[i][0]), markersize=85)  # S0
    line, = ax.plot([1.5], [2.5], marker="s",
                    color=cm.jet(V[i][1]), markersize=85)  # S1
    line, = ax.plot([2.5], [2.5], marker="s",
                    color=cm.jet(V[i][2]), markersize=85)  # S2
    line, = ax.plot([0.5], [1.5], marker="s",
                    color=cm.jet(V[i][3]), markersize=85)  # S3
    line, = ax.plot([1.5], [1.5], marker="s",
                    color=cm.jet(V[i][4]), markersize=85)  # S4
    line, = ax.plot([2.5], [1.5], marker="s",
                    color=cm.jet(V[i][5]), markersize=85)  # S5
    line, = ax.plot([0.5], [0.5], marker="s",
                    color=cm.jet(V[i][6]), markersize=85)  # S6
    line, = ax.plot([1.5], [0.5], marker="s",
                    color=cm.jet(V[i][7]), markersize=85)  # S7
    line, = ax.plot([2.5], [0.5], marker="s",
                    color=cm.jet(1.0), markersize=85)  # S8
    return (line,)


#@ú»ÖÆt[²ÆÌ`æÖðp¢Ä®æðì¬
anim = animation.FuncAnimation(
    fig, animate, init_func=init, frames=len(V), interval=200, repeat=False)

HTML(anim.to_jshtml())


Once Loop Reflect
 
