# ----------------------------------------------------------------------
# 定义棋子类型，输赢情况
# ----------------------------------------------------------------------
from const_set import *
import copy
# ----------------------------------------------------------------------
# 定义棋盘类，绘制棋盘的形状，切换先后手，判断输赢等
# ----------------------------------------------------------------------
class ChessBoard(object):
    def __init__(self):
        self.__board = [[EMPTY for n in range(N_LINE)] for m in range(N_LINE)]
        self.__dir = [[(-1, 0), (1, 0)], [(0, -1), (0, 1)], [(-1, 1), (1, -1)], [(-1, -1), (1, 1)]]
        #                (左      右)      (上       下)     (左下     右上)      (左上     右下)
        win_tree = []
        shape_score =[(50, (0, 1, 1, 0, 0)),
               (50, (0, 0, 1, 1, 0)),# live two
               (200, (1, 1, 0, 1, 0)),
               (200, (0, 1, 0, 1, 1)),
               (200, (1, 0, 1, 1, 0)),
               (200, (0, 1, 1, 0, 1)),
               (200, (1, 1, 0, 0, 1)),
               (200, (1, 0, 0, 1, 1)),
               (200, (1, 0, 1, 0, 1)),
               (500, (0, 0, 1, 1, 1)),
               (500, (1, 1, 1, 0, 0)),# sleep three
               (5000, (0, 1, 1, 1, 0)),
               (5000, (0, 1, 0, 1, 1, 0)),
               (5000, (0, 1, 1, 0, 1, 0)),# live three
               (7000, (1, 1, 1, 0, 1)),
               (7000, (1, 1, 0, 1, 1)),
               (7000, (1, 0, 1, 1, 1)),
               (7000, (1, 1, 1, 1, 0)),
               (7000, (0, 1, 1, 1, 1)),# sleep four
               (50000, (0, 1, 1, 1, 1, 0)),#live four
               (999999, (1, 1, 1, 1, 1))]

        shape_score_w = copy.deepcopy(shape_score)
        for i in range(len(shape_score_w)):
            www = []
            for j in range(len(shape_score_w[i][1])):
                www.append(shape_score_w[i][1][j] * 2)
            qqq = []
            qqq.append(shape_score_w[i][0])
            qqq.append(tuple(www))
            shape_score_w[i] = tuple(qqq)

        self.shape_score = shape_score
        self.shape_score_w  = shape_score_w

        # win_tree_vertical
        for i in range(N_LINE-4):
            for j in range(N_LINE):
                tmp = []
                for w in range(5):
                    tmp.append([i+w,j])
                win_tree.append(tmp)
        self.win_tree_vertical = len(win_tree)
        # win_tree_landscape
        for i in range(N_LINE):
            for j in range(N_LINE-4):
                tmp = []
                for w in range(5):
                    tmp.append([i,j+w])
                win_tree.append(tmp)
        self.win_tree_landscape = len(win_tree)

        # win_tree_oblique
        for i in range(N_LINE-4):
            for j in range(N_LINE-4):
                tmp = []
                for w in range(5):
                    tmp.append([i+w,j+w])
                win_tree.append(tmp)
        self.win_tree_oblique_1 = len(win_tree)

        for i in range(N_LINE-4):
            for j in range(4,N_LINE):
                tmp = []
                for w in range(5):
                    tmp.append([i+w,j-w])
                win_tree.append(tmp)

        self.win_tree_oblique_2 = len(win_tree)

        self.win_tree = win_tree






    def board(self):  # 返回数组对象
        return self.__board

    # def get_board_item(self):
    #     empty_item = []
    #     black = []
    #     white = []
    #     for i in range(MIDDLE,N_LINE + MIDDLE):
    #         for j in range(MIDDLE,N_LINE + MIDDLE):
    #             m = i % N_LINE
    #             n = j % N_LINE
    #             if self.__board[m][ns] == EMPTY:
    #                 empty_item.append([m,n])
    #             elif self.__board[m][n] == BLACK:
    #                 black.append([m,n])
    #             elif self.__board[m][n] == WHITE:
    #                 white.append([m,n])
    #     return empty_item,black,white

    def get_board_item(self):
        empty_item = []
        black = []
        white = []
        for i in range(MIDDLE,N_LINE + MIDDLE):
            for j in range(MIDDLE,N_LINE + MIDDLE):
                m = i % N_LINE
                n = j % N_LINE
                if self.__board[m][n] == EMPTY:
                    empty_item.append((m,n))
                elif self.__board[m][n] == BLACK:
                    black.append((m,n))
                elif self.__board[m][n] == WHITE:
                    white.append((m,n))
        return empty_item,black,white

    # def get_board_empty_tuples(self):
    #     empty_item = []

    #     for i in range(MIDDLE,N_LINE + MIDDLE):
    #         for j in range(MIDDLE,N_LINE + MIDDLE):
    #             m = i % N_LINE
    #             n = j % N_LINE
    #             if self.__board[m][n] == EMPTY:
    #                 empty_item.append((m,n))


    #     return empty_item





    def draw_xy(self, x, y, state):  # 获取落子点坐标的状态
        self.__board[x][y] = state

    def get_xy_on_logic_state(self, x, y):  # 获取指定点坐标的状态
        return self.__board[x][y]

    def get_next_xy(self, point, direction):  # 获取指定点的指定方向的坐标
        x = point[0] + direction[0]
        y = point[1] + direction[1]
        if x < 0 or x >= N_LINE or y < 0 or y >= N_LINE:
            return False
        else:
            return x, y

    def get_xy_on_direction_state(self, point, direction):  # 获取指定点的指定方向的状态
        if point is not False:
            xy = self.get_next_xy(point, direction)
            if xy is not False:
                x, y = xy
                return self.__board[x][y]
        return False

    def anyone_win(self, x, y):
        state = self.get_xy_on_logic_state(x, y) # 当前落下的棋是黑棋还是白棋，它的状态存储在state中
        for directions in self.__dir:  # 对米字的4个方向分别检测是否有5子相连的棋
            count = 1  # 初始记录为1，因为刚落下的棋也算
            for direction in directions:  # 对落下的棋子的同一条线的两侧都要检测，结果累积
                point = (x, y)  # 每次循环前都要刷新
                while True:
                    if self.get_xy_on_direction_state(point, direction) == state:
                        count += 1
                        point = self.get_next_xy(point, direction)
                    else:
                        break
            if count >= 5:
                return state
        e = self.get_board_item()[0]
        if len(e) == 0:
            return FULL
        return EMPTY


    def reset(self):  # 重置
        self.__board = [[EMPTY for n in range(N_LINE)] for m in range(N_LINE)]

    def closest_value(self,x,y):
        value = (x * (N_LINE - 1 - x) + y * (N_LINE - 1 - y)) / 5
        return value

    def get_k_dist_empty(self,k = 3):
        dist = k
        b = [[False for q in range(N_LINE)] for w in range(N_LINE)]
        empty_item = []
        for i in range(MIDDLE,N_LINE + MIDDLE):
            for j in range(MIDDLE,N_LINE + MIDDLE):
                m = i % N_LINE
                n = j % N_LINE
                if self.__board[m][n] is not EMPTY:
                    directions = [[1,0],[-1,0],[0,1],[0,-1],[1,-1],[-1,1],[1,1],[-1,-1]]
                    for t in range(1,k):
                        for direction in directions:
                            x_t = m + direction[0] * t
                            y_t = n + direction[1] * t
                            if x_t < 0 or x_t >= N_LINE or y_t < 0 or y_t >= N_LINE:
                                continue

                            if self.__board[x_t][y_t] == EMPTY and b[x_t][y_t] == False:
                                
                                b[x_t][y_t] = True
                                empty_item.append([x_t,y_t])


        return empty_item

    def get_k_dist_empty_tuple(self,k = 3):
        dist = k
        b = [[False for q in range(N_LINE)] for w in range(N_LINE)]
        empty_item = []
        for i in range(MIDDLE,N_LINE + MIDDLE):
            for j in range(MIDDLE,N_LINE + MIDDLE):
                m = i % N_LINE
                n = j % N_LINE
                if self.__board[m][n] is not EMPTY:
                    directions = [[1,0],[-1,0],[0,1],[0,-1],[1,-1],[-1,1],[1,1],[-1,-1]]
                    for t in range(1,k):
                        for direction in directions:
                            x_t = m + direction[0] * t
                            y_t = n + direction[1] * t
                            if x_t < 0 or x_t >= N_LINE or y_t < 0 or y_t >= N_LINE:
                                continue

                            if self.__board[x_t][y_t] == EMPTY and b[x_t][y_t] == False:
                                
                                b[x_t][y_t] = True
                                empty_item.append((x_t,y_t))


        return empty_item

    def value_judge(self,color):
        #          1,2,3,4,5
        b_sheet = [0,0,0,0,0]
        w_sheet = [0,0,0,0,0]
        # b_live_sheet = [0,0,0,0]
        # b_sleep_sheet = [0,0,0,0]
        # w_live_sheet = [0,0,0,0]
        # w_sleep_sheet = [0,0,0,0]
        shape_score = self.shape_score
        shape_score_w = self.shape_score_w





        win_tree = self.win_tree
        use_five_b = []
        b_value = 0
        w_value = 0
        for i in range(len(win_tree)):
            b_count = 0
            w_count = 0
            use_tmp = []
            has_black = False
            has_white = False
            for j in range(5):
                
                if self.get_xy_on_logic_state(win_tree[i][j][0],win_tree[i][j][1]) == BLACK:
                    has_black = True
                    b_count += 1
                elif self.get_xy_on_logic_state(win_tree[i][j][0],win_tree[i][j][1]) == WHITE:
                    has_white = True
                    w_count += 1
                use_tmp.append(self.get_xy_on_logic_state(win_tree[i][j][0],win_tree[i][j][1]))

                if has_black and has_white:
                    break
            #if has_black or has_white:
                
            if has_black and has_white:
                continue
            elif has_black == False and has_white == False:
                continue
            else:
                
                tup_5 = tuple(use_tmp)
                #print('tup:' + str(tup_5) + '  num:' + str(b_count))
                has_6 = False
                if i>=0 and i < self.win_tree_vertical:
                    direction = [1,0]
                if i >= self.win_tree_vertical and i < self.win_tree_landscape:
                    direction = [0,1]
                if i >= self.win_tree_landscape and i < self.win_tree_oblique_1:
                    direction = [1,1]
                if i >= self.win_tree_oblique_1 and i < len(win_tree):
                    direction = [1,-1]
                x_t = win_tree[i][j][0] + direction[0]
                y_t = win_tree[i][j][1] + direction[1]
                if not(x_t <0 or x_t >=N_LINE or y_t < 0 or y_t >= N_LINE):
                    if self.get_xy_on_logic_state(x_t,y_t) == EMPTY:
                        has_6 = True
                        use_tmp.append(EMPTY)
                        tup_6 = tuple(use_tmp)
                
                #print(tup_5)
            if has_black and b_count >= 2:


                for m in shape_score:
                    squ = m[1]
                    if len(squ) == 6 and has_6 == True:
                        if squ == tup_6:
                            if color == WHITE:
                                if m[0] == LIVE_THREE:
                                    b_value += m[0] * 5
                                if m[0] >= FOUR_VALUE:
                                    b_value += m[0] * 20
                            b_value += m[0]
                    elif len(squ) == 5:
                        if squ == tup_5:
                            if color == WHITE:
                                if m[0] == LIVE_THREE:
                                    b_value += m[0] * 5
                                if m[0] >= FOUR_VALUE:
                                    b_value += m[0] * 20
                            b_value += m[0]
                
            elif has_white and w_count >= 2:
                for m in shape_score_w:
                    squ = m[1]
                    if len(squ) == 6 and has_6 == True:
                        if squ == tup_6:
                            if color == BLACK:
                                if m[0] == LIVE_THREE:
                                    w_value += m[0] * 5
                                if m[0] >= FOUR_VALUE:
                                    w_value += m[0] * 20
                            w_value += m[0]
                    elif len(squ) == 5:
                        if squ == tup_5:
                            if color == BLACK:
                                if m[0] == LIVE_THREE:
                                    w_value += m[0] * 5
                                if m[0] >= FOUR_VALUE:
                                    w_value += m[0] * 20
                            w_value += m[0]
                



        # b_value = b_sheet[0] * ONE + b_sheet[1] * TWO + b_sheet[2] * THREE + b_sheet[3] * FOUR + b_sheet[4] * FIVE
        # w_value = w_sheet[0] * ONE + w_sheet[1] * TWO + w_sheet[2] * THREE + w_sheet[3] * FOUR + w_sheet[4] * FIVE

        for i in range(N_LINE):
            for j in range(N_LINE):
                if self.get_xy_on_logic_state(i,j) == BLACK:
                    b_value += self.closest_value(i,j)
                elif self.get_xy_on_logic_state(i,j) == WHITE:
                    w_value += self.closest_value(i,j)


        return b_value,w_value

    def value_judge_2(self,x,y,color): # for the step one
        shape_score = self.shape_score
        shape_score_w = self.shape_score_w





                


        b_value_after = 0
        b_value_before = 0
        w_value_after = 0
        w_value_before = 0

        # judge the 9 * 9
        point = (x,y)
        value_sheet_after = []
        value_sheet_before = []

        # landscape
        directions = [[1,0],[0,1],[1,-1],[1,1]]

        value_line_before = []
        for direction in directions:
            x_left = x - direction[0] * 4
            y_left = y - direction[1] * 4
            value_line = []
            value_line_before = []
            for i in range(9):
                x_t = x_left + i * direction[0]
                y_t = y_left + i * direction[1]
                if x_t < 0 or x_t >= N_LINE or y_t < 0 or y_t >= N_LINE:
                    continue
                value_line.append(self.get_xy_on_logic_state(x_t,y_t))
                if x_t == x and y_t == y:
                    value_line_before.append(EMPTY)
                else:
                    value_line_before.append(self.get_xy_on_logic_state(x_t,y_t))
            value_sheet_after.append(value_line)
            value_sheet_before.append(value_line_before)




        #value evaluate to the after one
        for i in range(len(value_sheet_after)):
            for j in range(len(shape_score)):
                ptr = 0
                while(1):
                    if ptr + len(shape_score[j][1]) >= 9:
                        break
                    tmp = tuple(value_sheet_after[i][ptr:(ptr+len(shape_score[j][1]))])
                    tmp_before = tuple(value_sheet_before[i][ptr:(ptr+len(shape_score[j][1]))])
                    ratio_b = 1
                    ratio_w = 1
                    if shape_score[j][0] >= FOUR_VALUE and color == BLACK:
                        ratio_w = 20
                    if shape_score[j][0] == LIVE_THREE and color == BLACK:
                        ratio_w = 5
                    if shape_score[j][0] >= FOUR_VALUE and color == WHITE:
                        ratio_b = 20
                    if shape_score[j][0] == LIVE_THREE and color == WHITE:
                        ratio_w = 5
                    if tmp == shape_score[j][1]:
                        b_value_after += shape_score[j][0] * ratio_b
                    if tmp_before == shape_score[j][1]:
                        b_value_before += shape_score[j][0] * ratio_b
                    if tmp == shape_score_w[j][1]:
                        w_value_after += shape_score_w[j][0] * ratio_w
                    if tmp_before == shape_score_w[j][1]:
                        w_value_before += shape_score_w[j][0] * ratio_w
                    ptr += 1

        b_value = b_value_after - b_value_before
        w_value = w_value_after - w_value_before
        closest_value = self.closest_value(x,y)
        color = self.get_xy_on_logic_state(x,y)
        if color == BLACK:
            b_value += closest_value
        elif color == WHITE:
           w_value += closest_value

        # print('b_value = ' + str(b_value))
        # print('w_value = ' + str(w_value))
        #print(x,y)

        return b_value,w_value







                













        








