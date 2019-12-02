#include"AI.h"

using namespace std;
//*******************************************************************
//*                       Method of AI                              *
//*******************************************************************
AI::AI(bool is_black, int depth, int cut_v = 10) {
	if (is_black) {
		color = BLACK;
		other = WHITE;
	}
	else {
		color = WHITE;
		other = BLACK;
	}
	my_depth = depth;
	cut = cut_v;
}
void AI::set(int depth, int cut_v = -1) {
	my_depth = depth;
	cut = cut_v;
}


int* AI::AI::get_move(chessboard board) {
	count = 0;
	int move[2] = { -1,-1 };
    v_idx tmp;
    tmp = Max(board, move, my_depth, 999999999);
//    if(my_depth <= 2){
//        tmp = Max(board, move, my_depth, 999999999);
//    }
//    else{
//        tmp = Max(board, move, my_depth*2, 999999999,true);
//        if(tmp.value < 9000000 && tmp.value > -9000000){
//            tmp = Max(board, move, my_depth, 999999999);
//        }
//    }

	move[0] = tmp.i;
	move[1] = tmp.j;
	static int move_r[2] = { 0,0 };
	move_r[0] = move[0];
	move_r[1] = move[1];
	return move_r;
}
v_idx AI::Max(chessboard board, int move[2], int depth, int cut_value,bool kill) {
	v_idx tmp;
	count++;

	tmp.i = move[0];
	tmp.j = move[1];
    int winner = -1;
	if (move[0] != -1) {
		board.draw(move[0], move[1], other);
        winner = board.anyone_win(move[0],move[1]);
        if (winner == color) {
			tmp.value = 9999999 * (depth + 1);
			return tmp;
		}
        if (winner == other) {
			tmp.value = -9999999 * (depth + 1);
			return tmp;
		}
        if(winner == FULL){
            tmp.value = 0;
            return tmp;
        }
	}

    vector<Point> empty_item = board.get_k_dist_empty(3, color, cut,kill);
    if(empty_item.size() == 0 && kill){
        tmp.value = 0;

        return tmp;
    }
	if (empty_item.size() == 0) {
		Point point;
		point.i = 7;
		point.j = 7;
		empty_item.push_back(point);
	}
	v_idx max_v_idx;
	max_v_idx.i = 0;
	max_v_idx.j = 0;
	max_v_idx.value = -999999999;
	depth--;
	if (depth < 0) {
		tmp.value = evaluate(board, color);
		return tmp;
	}
	v_idx result;
	int mov[2] = { 0,0 };
	for (int c = 0; c < empty_item.size(); c++) {
		mov[0] = empty_item[c].i;
		mov[1] = empty_item[c].j;
        result = Min(board, mov, depth, max_v_idx.value,kill);
		if (result.value > cut_value) {
			tmp.value = cut_value;
			return tmp;
		}
		if (max_v_idx.value < result.value) {
			max_v_idx.value = result.value;
			max_v_idx.i = mov[0];
			max_v_idx.j = mov[1];
		}

	}
	return max_v_idx;
}


v_idx AI::Min(chessboard board, int move[2], int depth, int cut_value,bool kill) {
	v_idx tmp;
	count++;

	tmp.i = move[0];
	tmp.j = move[1];
    int winner = -1;
	if (move[0] != -1) {
		board.draw(move[0], move[1], color);
        winner = board.anyone_win(move[0],move[1]);
        if (winner == color) {
            tmp.value = 9999999 * (depth + 1);
            return tmp;
        }
        if (winner == other) {
            tmp.value = -9999999 * (depth + 1);
            return tmp;
        }
        if(winner == FULL){
            tmp.value = 0;
            return tmp;
        }
	}
    vector<Point> empty_item = board.get_k_dist_empty(3, other, cut,kill);
    if(empty_item.size() == 0 && kill){
        tmp.value = 0;

        return tmp;
    }
	if (empty_item.size() == 0) {
		Point point;
		point.i = 7;
		point.j = 7;
		empty_item.push_back(point);
	}
	v_idx min_v_idx;
	min_v_idx.i = 0;
	min_v_idx.j = 0;
	min_v_idx.value = 999999999;
	depth--;
	if (depth < 0) {
		tmp.value = evaluate(board, color);
		return tmp;
	}
	v_idx result;
	int mov[2] = { 0,0 };
	for (int c = 0; c < empty_item.size(); c++) {
		mov[0] = empty_item[c].i;
		mov[1] = empty_item[c].j;
        result = Max(board, mov, depth, min_v_idx.value,kill);
		if (result.value < cut_value) {
			tmp.value = cut_value;
			return tmp;
		}
		if (min_v_idx.value > result.value) {
			min_v_idx.value = result.value;
			min_v_idx.i = mov[0];
			min_v_idx.j = mov[1];
		}

	}
	return min_v_idx;
}
int AI::evaluate(chessboard board, int color) {
	return board.value_judge_best(color);
}
