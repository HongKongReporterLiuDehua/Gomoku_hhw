#pragma once
#include"Point.h"
#include"v_idx.h"
#include"chessboard.h"
class AI {
public:
	int color;
	int other;
	int count;
	int my_depth;
    int cut = 10;
	AI(bool is_black, int depth, int cut_v);
	void set(int depth, int cut_v);
	int* get_move(chessboard board);
    v_idx Max(chessboard board, int move[2], int depth, int cut_value,bool kill=false);
    v_idx Min(chessboard board, int move[2], int depth, int cut_value,bool kill=false);
	int evaluate(chessboard board, int color);
};
