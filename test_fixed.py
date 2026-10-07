import turtle as tr
import random
import numpy as np
import keyboard

repeat = False
homecoord = np.array([[[220, 220], [140, 220], [220, 140], [140, 140]]])

endgame = np.array([[-10, 10], [10, 10], [10, -10], [-10, -10]])

pawnlist = ["1", "2", "3", "4"]
safepost = [4, 9, 17, 22, 30, 35, 43, 48, 53, 54, 55, 56, 57, 58]
md = 0

init = np.zeros((4, 4, 2))
players = np.zeros((4, 9))
players[:, 4] = [7, 20, 33, 46]

colour = ("red", "blue", "green", "yellow")
scolor = ("light blue", "light green", "orange", "pink")
ccolor = ("pink", "light blue", "light green", "orange")

sr = tr.Screen()
sr.setup(800, 800)

# ============================================================
# 🚀 MAXIMUM TURTLE SPEED
# ============================================================
tr.speed(0)
tr.tracer(0, 0)
# ============================================================


def count(r, l, p):
    tr.pu()
    tr.lt(90)
    tr.fd(r / 4)
    tr.rt(90)
    tr.bk(r / 4)
    tr.pd()

    if l == 0 or l == 3:
        tr.pencolor("black")
    elif l == 1 or l == 2:
        tr.pencolor("white")

    p += 1

    if r == 22:
        w = 22
    else:
        w = 10

    tr.write(str(p), font=("Kristen ITC", w, "bold"))
    tr.pencolor("black")


def rect(l, b):
    for _ in range(2):
        tr.fd(l)
        tr.rt(90)
        tr.fd(b)
        tr.rt(90)


def rst(l, b, c):
    tr.fillcolor(c)
    tr.begin_fill()
    tr.pencolor(c)
    rect(l, b)
    tr.pencolor("black")
    tr.end_fill()


def looptriangle():
    for _ in range(3):
        rect(40, 40)
        tr.fd(40)


def circle(r, c="black"):
    tr.pd()
    tr.color(c)
    tr.begin_fill()
    tr.circle(r)
    tr.end_fill()
    tr.pu()


def coordman(p, x=None, y=None):
    if x is None or y is None:
        raise ValueError("x and y coordinates are required")

    if p == 0:
        x = -x
    elif p == 1:
        pass
    elif p == 2:
        y = -y
    elif p == 3:
        x = -x
        y = -y

    return (x, y)


def initcord(p, c, r=None):
    temp = []

    for s in range(4):
        coords = init[s]
        temp.append(coordman(p, coords[0], coords[1]))

        if c is not None:
            tr.teleport(*temp[s])

    if r is not None:
        return temp[r]
    else:
        return temp


def positioncontrol(a, l=None, p=None):
    simp = a
    x = 0
    y = 0

    if 27 <= simp <= 32 or 40 <= simp <= 45:
        a -= 19

    elif 34 <= simp <= 39 or 47 <= simp <= 52:
        a -= 33

    if a == 0:
        x, y = init[l, p].flatten()
        y -= 12

    elif 1 <= a <= 6:
        x = -280 + 40 * (6 - a)
        y = -40

    elif 8 <= a <= 13:
        x = -280 + 40 * (a - 8)
        y = 40

    elif 14 <= a <= 19:
        x = -40
        y = 280 - 40 * (19 - a)

    elif 21 <= a <= 26:
        x = 40
        y = 280 - 40 * (a - 21)

    elif (simp - 7) % 13 == 0:

        if (simp - 7) / 13 == 0:
            x = -280

        elif (simp - 7) / 13 == 1:
            y = 280

        elif (simp - 7) / 13 == 2:
            x = 280

        elif (simp - 7) / 13 == 3:
            y = -280

    elif 53 <= a <= 57:
        lol = 240 - 40 * (a - 53)
        u = []

        if l == 0 or l == 2:
            u = coordman(l, lol, 0)
            x = u[0]

        elif l == 1 or l == 3:
            u = coordman(l, 0, lol)
            y = u[1]

    elif a == 58:
        x, y = endgame[p]

        if l == 0:
            x -= 40

        elif l == 1:
            y += 40

        elif l == 2:
            x += 40

        elif l == 3:
            y -= 40

    y -= 10
    x += md

    if 27 <= simp <= 32 or 34 <= simp <= 39:
        x = x + 360

    elif 40 <= simp <= 45 or 47 <= simp <= 52:
        y = y - 360

    return (x, y)


def engine(pno, tno, rollno):
    global md
    global repeat

    md = 0

    x, y = eraseloct[pno, tno]
    tr.teleport(x, y)

    r = 10

    if players[pno, tno] == 0:
        r = 22

    if 0 < players[pno, tno] < 53:
        c = ccolor[(int(players[pno, tno]) - 1) // 13]

    elif players[pno, tno] > 52 or players[pno, tno] == 0:
        c = ccolor[pno]

    circle(r, c)

    if players[pno, tno] != 0:

        tempost = players[pno, tno] + rollno
        players[pno, tno + 5] += rollno

        # calibration
        if tempost > 52:
            tempost -= 52

        if players[pno, tno + 5] > 52:
            tempost = players[pno, tno + 5]

        # collision control
        compare = players[:, :4].copy()
        compare[pno, :] = 0

        ml = list(np.where(compare == tempost))

        if tempost not in safepost and (compare == tempost).sum() > 0 and tempost < 53:

            players[ml[0], ml[1]] = 0

            eraseloct[ml[0], ml[1]] = positioncontrol(0, ml[0], ml[1])

            repeat = True

            tr.teleport(init[ml[0][0], ml[1][0], 0], init[ml[0][0], ml[1][0], 1] - 22)

            circle(22, colour[ml[0][0]])
            count(22, ml[0], ml[1][0])

        elif tempost in safepost[:8]:

            same = np.count_nonzero(players[:, :4] == tempost)

            md = 10 * same

        elif tempost in players[pno, :4] and tempost > 58:

            same = np.count_nonzero(players[pno, :4] == tempost)

            md = 10 * same

        players[pno, tno] = tempost

    elif rollno == 6:

        players[pno, tno] = players[pno, 4] + 2
        players[pno, tno + 5] = 2

    x, y = positioncontrol(players[pno, tno], pno, tno)

    if x != 0 or y != -10:

        eraseloct[pno, tno] = x, y

        tr.teleport(float(x), float(y))

        r = 10

        if players[pno, tno] == 0:
            r = 22

        circle(r, colour[pno])
        count(r, pno, tno)

    # 🚀 Render immediately after the move
    tr.update()


# ============================================================
# BOARD DRAWING
# ============================================================

tr.hideturtle()
tr.speed(0)

tr.pu()
tr.goto(-300, 300)
tr.pd()

tr.width(3)

rect(600, 600)

tr.color("black")

for ludo in range(4):

    tr.fillcolor(colour[ludo])
    tr.begin_fill()

    rect(240, 240)

    tr.end_fill()

    tr.pu()

    tr.fd(48)
    tr.rt(90)
    tr.fd(80)

    circle(32, ccolor[ludo])

    tr.fd(80)

    circle(32, ccolor[ludo])

    tr.lt(90)
    tr.fd(144)
    tr.lt(90)

    circle(32, ccolor[ludo])

    tr.fd(80)

    circle(32, ccolor[ludo])

    tr.fd(80)

    tr.rt(90)
    tr.fd(48)

    tr.pd()

    tr.color(0, 0, 0)
    tr.fillcolor(scolor[ludo])

    tr.begin_fill()

    for l in range(3):

        looptriangle()

        tr.rt(90)
        tr.fd(80)

        tr.rt(90)

        looptriangle()

        tr.lt(180)

    tr.rt(45)
    tr.fd(84.85281374238507)

    tr.lt(90)
    tr.fd(84.85281374238507)

    tr.pu()

    tr.lt(45)
    tr.fd(240)

    tr.rt(90)

    tr.end_fill()

    tr.fd(240)
    tr.rt(90)

    tr.pd()


# ============================================================
# INITIALIZE PAWNS
# ============================================================

for ludo in range(4):

    tx, ty = coordman(ludo, homecoord[0, :, 0], homecoord[0, :, 1])

    init[ludo, :4, 0] = tx
    init[ludo, :4, 1] = ty

    for c in range(4):

        tr.teleport(init[ludo, c, 0], init[ludo, c, 1] - 22)

        circle(22, colour[ludo])
        count(22, ludo, c)


eraseloct = init.copy()
eraseloct[:, :, 1] -= 22

# ============================================================
# 🚀 SHOW COMPLETE BOARD
# ============================================================

tr.update()

# ============================================================
# TESTING
# ============================================================

# engine(0, 0, 6)
# engine(1, 0, 6)
# engine(1, 0, 2)
# engine(0, 0, 15)
# engine(0, 2, 6)
# engine(0, 2, 56)
# engine(0, 3, 6)
# engine(0, 3, 55)

# print(players)

# ============================================================

tr.teleport(-335, -325)
rect(30, 30)

a = 0

while a < 1:

    playno = 0

    while playno < 4:

        repeat = False

        diceno = random.randint(1, 6)

        loop = 0

        tr.teleport(-335, -325)
        rst(30, 30, ccolor[playno])

        tr.teleport(-275, -320)
        rst(350, 30, "white")

        tr.teleport(-275, -350)

        tr.write("Press Space Bar to Roll the Dice ", font=("Harrington", 12, "normal"))

        tr.update()

        while loop < 1:

            if keyboard.read_key() == "space":
                loop = 1

            else:

                tr.teleport(-275, -320)

                rst(350, 30, "white")

                tr.teleport(-275, -350)

                tr.write(
                    "Oops,You press wrong key. Press 'space bar' to roll the Dice ",
                    font=("Harrington", 12, "normal"),
                )

                tr.update()

        if np.all((players[playno, 5:] + diceno) > 58):

            playno += 1
            continue

        loop = 0

        tr.teleport(-325, -355)

        tr.write(str(diceno), font=("Kristen ITC", 14, "bold"))

        tr.teleport(-275, -320)

        rst(450, 30, "white")

        tr.teleport(-275, -350)

        tr.write(
            "Choose btw 1, 2, 3, 4 to select the required pawn.",
            font=("Harrington", 12, "normal"),
        )

        tr.update()

        pawno = 2

        while loop < 1:

            pawno = keyboard.read_key()

            if pawno in pawnlist and (players[playno, int(pawno) + 4] + diceno) <= 58:

                loop = 2

        engine(playno, int(pawno) - 1, diceno)

        if np.all(players[playno, :4] == 58):

            a = 2
            break

        if diceno != 6 and repeat == False:
            playno += 1


# ============================================================
# WINNER
# ============================================================

tr.teleport(-400, -320)

rst(650, 30, "white")

tr.teleport(-275, -350)

tr.pencolor(colour[playno])

tr.write("Player " + colour[playno] + " has won.", font=("Harrington", 12, "normal"))

tr.update()

tr.done()
