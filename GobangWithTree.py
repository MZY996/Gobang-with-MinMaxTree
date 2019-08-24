from graphics import *
from math import *
import numpy as np
##import time
import random2
import xlrd
import xlsxwriter

GRID_WIDTH = 40
COLUMN = 15
ROW = 15

list1 = []  # AI
list2 = []  # human
list3 = []  # all

list_all = []  # 整个棋盘的点
next_point = [0, 0]  # AI下一步最应该下的位置

ratio = 1  # 进攻的系数   大于1 进攻型，  小于1 防守型
DEPTH = 1  # 搜索深度   只能是单数。  如果是负数， 评估函数评估的的是自己多少步之后的自己得分的最大值，并不意味着是最好的棋， 评估函数的问题

# b1=50
# b2=50
# c1=200
# c2=500
# c3=500
# c4=5000
# c5=5000
# c6=5000
# d1=5000
# d2=5000
# d3=5000
# d4=5000
# d5=5000
# d6=50000
ExcelFile=xlrd.open_workbook(r'D:\107工程\大创\gobang_AI-master\score.xlsx')
sheet=ExcelFile.sheet_by_index(0)
score=[sheet.cell_value(0,0),sheet.cell_value(1,0),sheet.cell_value(2,0),sheet.cell_value(3,0),sheet.cell_value(4,0),sheet.cell_value(5,0),sheet.cell_value(6,0),sheet.cell_value(7,0),sheet.cell_value(8,0),sheet.cell_value(9,0),sheet.cell_value(10,0),sheet.cell_value(11,0),sheet.cell_value(12,0),sheet.cell_value(13,0)]
# 棋型的评估分数
##print(score)
# workbook = xlsxwriter.Workbook(r'D:\107工程\大创\gobang_AI-master\score.xlsx')
# newsheet = workbook.add_worksheet()
# for i in range(0, len(score)):
#     newsheet.write(i,0,88)
# workbook.close()
shape_score = [(score[0], (0, 1, 1, 0, 0)),
               (score[1], (0, 0, 1, 1, 0)),
               (score[2], (1, 1, 0, 1, 0)),
               (score[3], (0, 0, 1, 1, 1)),
               (score[4], (1, 1, 1, 0, 0)),
               (score[5], (0, 1, 1, 1, 0)),
               (score[6], (0, 1, 0, 1, 1, 0)),
               (score[7], (0, 1, 1, 0, 1, 0)),
               (score[8], (1, 1, 1, 0, 1)),
               (score[9], (1, 1, 0, 1, 1)),
               (score[10], (1, 0, 1, 1, 1)),
               (score[11], (1, 1, 1, 1, 0)),
               (score[12], (0, 1, 1, 1, 1)),
               (score[13], (0, 1, 1, 1, 1, 0)),
               (99999990, (1, 1, 1, 1, 1))]
usageSheet=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

def ai():  ##启发式学习改
    global cut_count   # 统计剪枝次数
    cut_count = 0
    global search_count   # 统计搜索次数
    search_count = 0
    negamax(True, DEPTH, -99999999, 99999999)
    ##print("本次共剪枝次数：" + str(cut_count))
    ##print("本次共搜索次数：" + str(search_count))
    # next_step=(next_point[0], next_point[1])
    # list1.append(next_step)
    # list3.append(next_step)
    # negamax(True, 2, -99999999, 99999999)
    # list1.remove(next_step)
    # list3.remove(next_step)
    return next_point[0],next_point[1]

def anotherAI():  ##启发式学习改
    global cut_count   # 统计剪枝次数
    cut_count = 0
    global search_count   # 统计搜索次数
    search_count = 0
    negamax(False, DEPTH, -99999999, 99999999)
    ##print("本次共剪枝次数：" + str(cut_count))
    ##print("本次共搜索次数：" + str(search_count))
    # next_step=(next_point[0], next_point[1])
    # list1.append(next_step)
    # list3.append(next_step)
    # negamax(False, 2, -99999999, 99999999)
    # list1.remove(next_step)
    # list3.remove(next_step)
    return next_point[0],next_point[1]

# 负值极大算法搜索 alpha + beta剪枝
def negamax(is_ai, depth, alpha, beta):
    # 游戏是否结束 | | 探索的递归深度是否到边界
    if game_win(list1) or game_win(list2) or depth == 0:
        return evaluation(is_ai)

    blank_list = list(set(list_all).difference(set(list3)))
    order(blank_list)   # 搜索顺序排序  提高剪枝效率
    # 遍历每一个候选步
    for next_step in blank_list:

        global search_count
        search_count += 1

        # 如果要评估的位置没有相邻的子， 则不去评估  减少计算
        if not has_neightnor(next_step):
            continue

        if is_ai:
            list1.append(next_step)
        else:
            list2.append(next_step)
        list3.append(next_step)

        value = -negamax(not is_ai, depth - 1, -beta, -alpha)
        if is_ai:
            list1.remove(next_step)
        else:
            list2.remove(next_step)
        list3.remove(next_step)

        if value > alpha:

            ##print(str(value) + "alpha:" + str(alpha) + "beta:" + str(beta))
            ##print(list3)
            if depth == DEPTH:
                next_point[0] = next_step[0]
                next_point[1] = next_step[1]
            # alpha + beta剪枝点
            if value >= beta:
                global cut_count
                cut_count += 1
                return beta
            alpha = value

    return alpha


#  离最后落子的邻居位置最有可能是最优点
def order(blank_list):
    last_pt = list3[-1]
    for item in blank_list:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if (last_pt[0] + i, last_pt[1] + j) in blank_list:
                    blank_list.remove((last_pt[0] + i, last_pt[1] + j))
                    blank_list.insert(0, (last_pt[0] + i, last_pt[1] + j))


def has_neightnor(pt):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if (pt[0] + i, pt[1]+j) in list3:
                return True
    return False


# 评估函数
def evaluation(is_ai):
    total_score = 0

    if is_ai:
        my_list = list1
        enemy_list = list2
    else:
        my_list = list2
        enemy_list = list1

    # 算自己的得分
    score_all_arr = []  # 得分形状的位置 用于计算如果有相交 得分翻倍
    my_score = 0
    for pt in my_list:
        m = pt[0]
        n = pt[1]
        my_score += cal_score(m, n, 0, 1, enemy_list, my_list, score_all_arr)
        my_score += cal_score(m, n, 1, 0, enemy_list, my_list, score_all_arr)
        my_score += cal_score(m, n, 1, 1, enemy_list, my_list, score_all_arr)
        my_score += cal_score(m, n, -1, 1, enemy_list, my_list, score_all_arr)

    #  算敌人的得分， 并减去
    score_all_arr_enemy = []
    enemy_score = 0
    for pt in enemy_list:
        m = pt[0]
        n = pt[1]
        enemy_score += cal_score(m, n, 0, 1, my_list, enemy_list, score_all_arr_enemy)
        enemy_score += cal_score(m, n, 1, 0, my_list, enemy_list, score_all_arr_enemy)
        enemy_score += cal_score(m, n, 1, 1, my_list, enemy_list, score_all_arr_enemy)
        enemy_score += cal_score(m, n, -1, 1, my_list, enemy_list, score_all_arr_enemy)

    total_score = my_score - enemy_score*ratio*0.1

    return total_score


# 每个方向上的分值计算
def cal_score(m, n, x_direction, y_direction, enemy_list, my_list, score_all_arr):
    add_score = 0  # 加分项
    # 在一个方向上， 只取最大的得分项
    max_score_shape = (0, None)

    # 如果此方向上，该点已经有得分形状，不重复计算
    for item in score_all_arr:
        for pt in item[1]:
            if m == pt[0] and n == pt[1] and x_direction == item[2][0] and y_direction == item[2][1]:
                return 0

    # 在落子点 左右方向上循环查找得分形状
    for offset in range(-5, 1):
        # offset = -2
        pos = []
        for i in range(0, 6):
            if (m + (i + offset) * x_direction, n + (i + offset) * y_direction) in enemy_list:
                pos.append(2)
            elif (m + (i + offset) * x_direction, n + (i + offset) * y_direction) in my_list:
                pos.append(1)
            else:
                pos.append(0)
        tmp_shap5 = (pos[0], pos[1], pos[2], pos[3], pos[4])
        tmp_shap6 = (pos[0], pos[1], pos[2], pos[3], pos[4], pos[5])
        # print(pos) ##############################################################################################
        #print(tmp_shap5)
        for i in range (0,14):
            if tmp_shap5 == shape_score[i][1] or tmp_shap6 == shape_score[i][1]:
                if tmp_shap5 == (1,1,1,1,1):
                    print('4连！')
                if shape_score[i][0] > max_score_shape[0]:
                    max_score_shape = (shape_score[i][0], ((m + (0+offset) * x_direction, n + (0+offset) * y_direction),
                                               (m + (1+offset) * x_direction, n + (1+offset) * y_direction),
                                               (m + (2+offset) * x_direction, n + (2+offset) * y_direction),
                                               (m + (3+offset) * x_direction, n + (3+offset) * y_direction),
                                               (m + (4+offset) * x_direction, n + (4+offset) * y_direction)), (x_direction, y_direction))

    # 计算两个形状相交， 如两个3活 相交， 得分增加 一个子的除外
    if max_score_shape[1] is not None:
        for item in score_all_arr:
            for pt1 in item[1]:
                for pt2 in max_score_shape[1]:
                    if pt1 == pt2 and max_score_shape[0] > 10 and item[0] > 10:
                        add_score += item[0] + max_score_shape[0]

        score_all_arr.append(max_score_shape)
    ##print(add_score + max_score_shape[0])
    return add_score + max_score_shape[0]


def game_win(list):
    for m in range(COLUMN):
        for n in range(ROW):

            if n < ROW - 4 and (m, n) in list and (m, n + 1) in list and (m, n + 2) in list and (
                    m, n + 3) in list and (m, n + 4) in list:
                return True
            elif m < ROW - 4 and (m, n) in list and (m + 1, n) in list and (m + 2, n) in list and (
                        m + 3, n) in list and (m + 4, n) in list:
                return True
            elif m < ROW - 4 and n < ROW - 4 and (m, n) in list and (m + 1, n + 1) in list and (
                        m + 2, n + 2) in list and (m + 3, n + 3) in list and (m + 4, n + 4) in list:
                return True
            elif m < ROW - 4 and n > 3 and (m, n) in list and (m + 1, n - 1) in list and (
                        m + 2, n - 2) in list and (m + 3, n - 3) in list and (m + 4, n - 4) in list:
                return True
    return False


def gobangwin():
    win = GraphWin("Gomoku with MinMaxTree", GRID_WIDTH * COLUMN, GRID_WIDTH * ROW)
    win.setBackground("grey")   ##棋盘颜色
    i1 = 0

    while i1 <= GRID_WIDTH * COLUMN:
        l = Line(Point(i1, 0), Point(i1, GRID_WIDTH * COLUMN))
        l.draw(win)
        i1 = i1 + GRID_WIDTH
    i2 = 0

    while i2 <= GRID_WIDTH * ROW:
        l = Line(Point(0, i2), Point(GRID_WIDTH * ROW, i2))
        l.draw(win)
        i2 = i2 + GRID_WIDTH
    return win


def main():
    win = gobangwin()

    for i in range(COLUMN+1):
        for j in range(ROW+1):
            list_all.append((i, j))

    change = 0
    state = 0  ##state=0表示游戏进行
    m = 0
    n = 0
    global lastpiece

    while state == 0:
        if change == 1:     #AI的第一步在棋盘中间随机取点下，避免开局一成不变
            # win.getMouse()
            pos=(random2.randrange(8,9),random2.randrange(8,9))
            while pos==list2[0]:      ##避免随机点与玩家的第一个点相同
                pos = (random2.randrange(4, 12), random2.randrange(4, 12))
            # print(list2[0])
            # print(pos)
            list1.append(pos)
            list3.append(pos)
            piece = Circle(Point(GRID_WIDTH * pos[0], GRID_WIDTH * pos[1]), 16)
            piece.setFill('Red')
            global lastpiece
            lastpiece=piece
            piece.draw(win)
            change=change+1

        elif change % 2 == 1 and change > 2:  ##change为单数则轮到AI下
            pos = ai()    ##获得AI判断的下一步
            if pos in list3:
                message = Text(Point(200, 200), "不可用的位置" + str(pos[0]) + "," + str(pos[1]))
                message.draw(win)
                state = 1

            list1.append(pos)
            list3.append(pos)

            piece = Circle(Point(GRID_WIDTH * pos[0], GRID_WIDTH * pos[1]), 16)
            piece.setFill('Red')

            if change>2:
                lastpiece.setFill('white')
            lastpiece = piece
            piece.draw(win)

            if game_win(list1):
                message = Text(Point(100, 100), "Winner: White")
                message.draw(win)
                state = 1    ##AI赢了，state=1 游戏结束
            change = change + 1

        else:  ##轮到玩家下
            p2 = win.getMouse()
            if not ((round((p2.getX()) / GRID_WIDTH), round((p2.getY()) / GRID_WIDTH)) in list3):

                a2 = round((p2.getX()) / GRID_WIDTH)
                b2 = round((p2.getY()) / GRID_WIDTH)
                list2.append((a2, b2))
                list3.append((a2, b2))
                piece = Circle(Point(GRID_WIDTH * a2, GRID_WIDTH * b2), 16)

                piece.setFill('black')
                piece.draw(win)
                if game_win(list2):
                    message = Text(Point(100, 100), "Winner: Black")
                    message.draw(win)
                    state = 1

                change = change + 1

    message = Text(Point(100, 120), "Click anywhere to quit.")
    message.draw(win)
    win.getMouse()
    win.close()
####################################training part#######################################
#########################################################################################
def evaluationX(is_ai):
    total_score = 0

    if is_ai:
        my_list = list1
        enemy_list = list2
    else:
        my_list = list2
        enemy_list = list1

    # 算自己的得分
    score_all_arr = []  # 得分形状的位置 用于计算如果有相交 得分翻倍
    my_score = 0
    for pt in my_list:
        m = pt[0]
        n = pt[1]
        my_score += cal_scoreX(m, n, 0, 1, enemy_list, my_list, score_all_arr)
        my_score += cal_scoreX(m, n, 1, 0, enemy_list, my_list, score_all_arr)
        my_score += cal_scoreX(m, n, 1, 1, enemy_list, my_list, score_all_arr)
        my_score += cal_scoreX(m, n, -1, 1, enemy_list, my_list, score_all_arr)

    #  算敌人的得分， 并减去
    score_all_arr_enemy = []
    enemy_score = 0
    for pt in enemy_list:
        m = pt[0]
        n = pt[1]
        enemy_score += cal_scoreX(m, n, 0, 1, my_list, enemy_list, score_all_arr_enemy)
        enemy_score += cal_scoreX(m, n, 1, 0, my_list, enemy_list, score_all_arr_enemy)
        enemy_score += cal_scoreX(m, n, 1, 1, my_list, enemy_list, score_all_arr_enemy)
        enemy_score += cal_scoreX(m, n, -1, 1, my_list, enemy_list, score_all_arr_enemy)

    total_score = my_score - enemy_score*ratio*0.1
    print(usageSheet)
    return total_score


# 每个方向上的分值计算
def cal_scoreX(m, n, x_direction, y_direction, enemy_list, my_list, score_all_arr):
    add_score = 0  # 加分项
    # 在一个方向上， 只取最大的得分项
    max_score_shape = (0, None)

    # 如果此方向上，该点已经有得分形状，不重复计算
    for item in score_all_arr:
        for pt in item[1]:
            if m == pt[0] and n == pt[1] and x_direction == item[2][0] and y_direction == item[2][1]:
                return 0

    # 在落子点 左右方向上循环查找得分形状
    for offset in range(-5, 1):
        # offset = -2
        pos = []
        for i in range(0, 6):
            if (m + (i + offset) * x_direction, n + (i + offset) * y_direction) in enemy_list:
                pos.append(2)
            elif (m + (i + offset) * x_direction, n + (i + offset) * y_direction) in my_list:
                pos.append(1)
            else:
                pos.append(0)
        tmp_shap5 = (pos[0], pos[1], pos[2], pos[3], pos[4])
        tmp_shap6 = (pos[0], pos[1], pos[2], pos[3], pos[4], pos[5])
        # print(pos) ##############################################################################################
        #print(tmp_shap5)
        for i in range (0,14):
            if tmp_shap5 == shape_score[i][1] or tmp_shap6 == shape_score[i][1]:
                if tmp_shap5 == (1,1,1,1,1):
                    print('4连！')
                if shape_score[i][0] > max_score_shape[0]:
                    usageSheet[i] += 1
                    max_score_shape = (shape_score[i][0], ((m + (0+offset) * x_direction, n + (0+offset) * y_direction),
                                               (m + (1+offset) * x_direction, n + (1+offset) * y_direction),
                                               (m + (2+offset) * x_direction, n + (2+offset) * y_direction),
                                               (m + (3+offset) * x_direction, n + (3+offset) * y_direction),
                                               (m + (4+offset) * x_direction, n + (4+offset) * y_direction)), (x_direction, y_direction))

    # 计算两个形状相交， 如两个3活 相交， 得分增加 一个子的除外
    if max_score_shape[1] is not None:
        for item in score_all_arr:
            for pt1 in item[1]:
                for pt2 in max_score_shape[1]:
                    if pt1 == pt2 and max_score_shape[0] > 10 and item[0] > 10:
                        add_score += item[0] + max_score_shape[0]

        score_all_arr.append(max_score_shape)
    ##print(add_score + max_score_shape[0])
    return add_score + max_score_shape[0]


def train():  ##训练，AI与AI下
    win = gobangwin()

    for i in range(COLUMN+1):
        for j in range(ROW+1):
            list_all.append((i, j))

    change = 0
    state = 0  ##state=0表示游戏进行
    m = 0
    n = 0
    global lastpiece

    while state == 0:
        if change == 0:
            # win.getMouse()
            pos = (random2.randrange(8, 9), random2.randrange(8, 9))
            list2.append(pos)
            list3.append(pos)
            piece = Circle(Point(GRID_WIDTH * pos[0], GRID_WIDTH * pos[1]), 16)
            piece.setFill('black')

            piece.draw(win)
            change = change + 1

        elif change == 1:
            # win.getMouse()
            pos = (random2.randrange(6, 9), random2.randrange(5, 8))
            while pos==list2[0]:      ##避免随机点与黑子的第一个点相同
                pos = (random2.randrange(7, 9), random2.randrange(7, 10))
            list1.append(pos)
            list3.append(pos)
            piece = Circle(Point(GRID_WIDTH * pos[0], GRID_WIDTH * pos[1]), 16)
            piece.setFill('red')
            global lastpiece
            lastpiece=piece

            piece.draw(win)
            change = change + 1

        elif change % 2 == 1 and change>2 : ##change为单数则轮到AI下
            pos = ai()
            if pos in list3:
                message = Text(Point(200, 200), "不可用的位置" + str(pos[0]) + "," + str(pos[1]))
                message.draw(win)
                state = 1

            list1.append(pos)
            list3.append(pos)

            piece = Circle(Point(GRID_WIDTH * pos[0], GRID_WIDTH * pos[1]), 16)
            piece.setFill('Red')


            if change>2:
                lastpiece.setFill('white')
                lastpiece = piece
            lastpiece = piece
            piece.draw(win)

            if game_win(list1):
                message = Text(Point(100, 100), "Winner: White")
                message.draw(win)
                state = 1    ##AI赢了，state=1 游戏结束
                evaluationX(0)
            change = change + 1

        else:
            # win.getMouse()
            a2,b2 = anotherAI();
            list2.append((a2, b2))
            list3.append((a2, b2))
            piece = Circle(Point(GRID_WIDTH * a2, GRID_WIDTH * b2), 16)

            piece.setFill('black')
            piece.draw(win)
            if game_win(list2):
                message = Text(Point(100, 100), "Winner: Black")
                message.draw(win)      #AI输了，要进行训练
                evaluationX(1)
                state = 1
                workbook = xlsxwriter.Workbook(r'D:\107工程\大创\gobang_AI-master\score.xlsx')
                newsheet = workbook.add_worksheet()
                for i in range(0, len(score)):
                    newsheet.write(i,0,score[i]*2/(usageSheet[i]+1))
                workbook.close()

            change = change + 1

    message = Text(Point(100, 120), "Click anywhere to quit.")
    message.draw(win)
    win.getMouse()
    win.close()

train()
# main()