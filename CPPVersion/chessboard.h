#pragma once
#include"const.h"

using namespace std;
class chessboard {
public:
	int board[15][15];
	int dir[4][2] = { { 1,0 },{ 0,1 },{ 1,-1 },{ 1,1 } };
	int black_value[15][15];
	int white_value[15][15];
	int black_value_idx[15][15][4];
	int white_value_idx[15][15][4];
	chessboard(int board_tmp[15][15], int black_value_idx_tmp[15][15][4], int white_value_idx_tmp[15][15][4]);
    chessboard();
    void clear();
	//bool cmpy_w(Point a, Point b);
	//bool cmpy_b(Point a, Point b);
	void draw(int i, int j, int color);

    vector<Point> get_k_dist_empty(int k, int color, int cut,bool kill);
	int anyone_win(int x, int y);
	void value_change_after_draw(int i, int j);
	void one_point_value_update(int i, int j, int dir_idx);
	int value_judge_best(int color);
	int score_polish(int score);
	int* one_point_value(int i, int j, int color, int dir_idx);
	int one_point_value_one_dir(int i, int j, int color, int dir_idx);
	int countToScore(int count, int empty, bool block_l, bool block_r);
	bool isInBoard(int i, int j);
	int get_the_color(int i, int j);
    UI_board showBoard();

};
