#include"chessboard.h"

using namespace std;

bool cmpy(Point a, Point b) {
	return a.black_value + a.white_value > b.black_value + b.white_value;
}

//*******************************************************************
//*                       Method of Chessboard                      *
//*******************************************************************
chessboard::chessboard(){

    clear();


}
chessboard::chessboard(int board_tmp[15][15], int black_value_idx_tmp[15][15][4], int white_value_idx_tmp[15][15][4]) {
	memcpy(board, board_tmp, sizeof(board_tmp) * 225);
	memcpy(black_value_idx, black_value_idx_tmp, sizeof(black_value_idx_tmp) * 15 * 15 * 4);
	memcpy(white_value_idx, white_value_idx_tmp, sizeof(white_value_idx_tmp) * 15 * 15 * 4);

	//cout << "tmp" << board_tmp[0][6] << endl;
	//cout << board[0][6] << endl;
	//cout << black_value_idx[2][2][2] << endl;
	//cout << black_value_idx_tmp[2][2][2] << endl;
	int tmp1 = 0;
	int tmp2 = 0;
	for (int i = 0; i < 15; i++) {
		for (int j = 0; j < 15; j++) {
			tmp1 = 0;
			tmp2 = 0;
			for (int m = 0; m < 4; m++) {
				tmp1 += black_value_idx[i][j][m];
				tmp2 += white_value_idx[i][j][m];

			}
			black_value[i][j] = tmp1;
			white_value[i][j] = tmp2;
		}
	}
	cout << "C++ AI init over!" << endl;

}
void chessboard::clear() {
	for (int i = 0; i < 15; i++) {
		for (int j = 0; j < 15; j++) {
			board[i][j] = 0;
			for (int m = 0; m < 4; m++) {
				black_value_idx[i][j][m] = 0;
				white_value_idx[i][j][m] = 0;
			}
			black_value[i][j] = 0;
			white_value[i][j] = 0;
		}
	}
}
bool chessboard::isInBoard(int i, int j) {
	if (i < 0 || i >= 15 || j < 0 || j >= 15) {
		return false;
	}
	return true;
}

vector<Point> chessboard::get_k_dist_empty(int k, int color, int cut,bool kill) {
	int b[15][15];
	Point tmp;
	vector<Point> empty_set;
	for (int i = 0; i < 15; i++) {
		for (int j = 0; j < 15; j++) {
			b[i][j] = 2;
		}
	}
	bool HasIn = false;
	int i_d = 0;
	int j_d = 0;
	int m = 0;
	int n = 0;
	bool isIn = false;
	for (int i = 7; i < 22; i++) {
		for (int j = 7; j < 22; j++) {
			m = i % 15;
			n = j % 15;
			if (board[m][n] != EMPTY) {
				for (int d = 0; d < 4; d++) {
					HasIn = false;
					for (int dist = -k + 1; dist < k; dist++) {
						if (dist == 0) {
							continue;
						}
						i_d = m + dir[d][0] * dist;
						j_d = n + dir[d][1] * dist;
						isIn = isInBoard(i_d, j_d);
						if (isIn == false && HasIn == true) {
							break;
						}
						if (isIn == false && HasIn == false) {
							continue;
						}
						if (isIn == true) {
							HasIn = true;
							if (board[i_d][j_d] == EMPTY && b[i_d][j_d] > 0) {
								b[i_d][j_d] -= 1;
								if (b[i_d][j_d] == 0) {
									tmp.i = i_d;
									tmp.j = j_d;
									tmp.black_value = score_polish(black_value[i_d][j_d]);
									tmp.white_value = score_polish(white_value[i_d][j_d]);
									empty_set.push_back(tmp);
								}
							}
						}

					}
				}
			}

		}
	}
	if (empty_set.empty()) {
		if (board[7][7] == EMPTY) {
			tmp.i = 7;
			tmp.j = 7;
			tmp.black_value = score_polish(black_value[7][7]);
			tmp.white_value = score_polish(white_value[7][7]);
			empty_set.push_back(tmp);
		}
		else {
			int delta_i = 0;
			int delta_j = 0;
			while (1) {
				int r_num[3] = { -1,0,1 };
				delta_i = r_num[rand() % 3];
				delta_j = r_num[rand() % 3];
				if (board[7 + delta_i][7 + delta_j] == EMPTY) {
					tmp.i = 7 + delta_i;
					tmp.j = 7 + delta_j;
					tmp.black_value = score_polish(black_value[7 + delta_i][7 + delta_j]);
					tmp.white_value = score_polish(white_value[7 + delta_i][7 + delta_j]);
					empty_set.push_back(tmp);
					break;
				}
			}
		}
		return empty_set;
	}
	if (color == EMPTY) {
		return empty_set;
	}

	sort(empty_set.begin(), empty_set.end(), cmpy);
    if(kill){
        int mmm = 0;
        for(mmm = 0; mmm < empty_set.size();mmm++){
            if(empty_set[mmm].black_value + empty_set[mmm].white_value < THREE){
                break;
            }
            if(mmm == 3)break;
        }
        empty_set.erase(empty_set.begin() + mmm, empty_set.end());
        return empty_set;
    }


	if (empty_set.size() > cut && cut != -1) {
		empty_set.erase(empty_set.begin() + cut, empty_set.end());
	}
	return empty_set;

}






void chessboard::draw(int i, int j, int color) {
	if (isInBoard(i, j)) {
		if (board[i][j] == EMPTY) {
			board[i][j] = color;
			value_change_after_draw(i, j);
		}
		else {
			cout << "Not empty" << i << "," << j << "color: " << color << endl;
		}
	}
	else {
		cout << "The draw Out of the board!" << endl;
	}
}
int chessboard::anyone_win(int i, int j) {
	int state = board[i][j];
	if (state == BLACK) {
		if (black_value[i][j] >= FIVE) {
			return BLACK;
		}
	}
	if (state == WHITE) {
		if (white_value[i][j] >= FIVE) {
			return WHITE;
		}
	}

	for (int m = 0; m < 15; m++) {
		for (int n = 0; n < 15; n++) {
			if (board[m][n] == EMPTY) {
				return EMPTY;
			}
		}
	}
	return FULL;

}

int chessboard::one_point_value_one_dir(int i, int j, int color, int dir_idx) {
	//dir = [(1,0),(0,1),(1,-1),(1,1)]
	int value = 0;
	int this_color = color;
	int value_dir[4] = { 0,0,0,0 };
	int this_dir[2];
	if (dir_idx >= 0 && dir_idx <= 3) {
		this_dir[0] = dir[dir_idx][0];
		this_dir[1] = dir[dir_idx][1];
	}
	else {
		return 0;
	}
	int count = 1;
	int second_count = 0;
	int empty = -1;
	bool block_l = false;
	bool block_r = false;
	int i_t, j_t;
	int the_color;
	int i_t_t, j_t_t;
	i_t = this_dir[0] + i;
	j_t = this_dir[1] + j;
	while (1) {
		the_color = get_the_color(i_t, j_t);
		if (the_color == OUT) {
			block_l = true;
			break;
		}
		i_t_t = i_t + this_dir[0];
		j_t_t = j_t + this_dir[1];
		if (the_color == EMPTY) {
			if (empty == -1 && get_the_color(i_t_t, j_t_t) == this_color) {
				empty = count;
			}
			else {
				break;
			}
		}
		else if (the_color == this_color) {
			count += 1;
		}
		else {
			block_l = true;
			break;
		}
		i_t = i_t_t;
		j_t = j_t_t;
	}

	i_t = -this_dir[0] + i;
	j_t = -this_dir[1] + j;
	while (1) {
		the_color = get_the_color(i_t, j_t);
		if (the_color == OUT) {
			block_r = true;
			break;
		}
		i_t_t = i_t - this_dir[0];
		j_t_t = j_t - this_dir[1];
		if (the_color == EMPTY) {
			if (empty == -1 && get_the_color(i_t_t, j_t_t) == this_color) {
				empty = 0;
			}
			else {
				break;
			}
		}
		else if (the_color == this_color) {
			second_count += 1;
			if (empty != -1) {
				empty++;
			}
		}
		else {
			block_r = true;
			break;
		}
		i_t = i_t_t;
		j_t = j_t_t;
	}
	count += second_count;
	value = countToScore(count, empty, block_l, block_r);
	return value;
}
int* chessboard::one_point_value(int i, int j, int color, int dir_idx) {
	int value[4];
	for (int c = 0; c < 4; c++) {
		value[c] = one_point_value_one_dir(i, j, color, c);
	}
	static int value_r[4];
	value_r[0] = value[0];
	value_r[1] = value[1];
	value_r[2] = value[2];
	value_r[3] = value[3];
	return value_r;
}
int chessboard::get_the_color(int i, int j) {
	if (isInBoard(i, j)) {
		return board[i][j];
	}
	return OUT;
}
int chessboard::countToScore(int count, int empty, bool block_l, bool block_r) {
	int block = 0;
	if (block_l) {
		block++;
	}
	if (block_r) {
		block++;
	}
	if (empty <= 0) {
		if (count >= 5) {
			return FIVE;
		}
		if (block == 0) {
			switch (count) {
			case 1:return ONE;
			case 2:return TWO;
			case 3:return THREE;
			case 4:return FOUR;
			}
		}
		else if (block == 1) {
			switch (count) {
			case 1:return BLOCK_ONE;
			case 2:return BLOCK_TWO;
			case 3:return BLOCK_THREE;
			case 4:return BLOCK_FOUR;
			}
		}
	}
	else if (empty == 1 || empty == count - 1) {
		if (count >= 6) {
			return FIVE;
		}
		if (block == 0) {
			switch (count) {
			case 2:return TWO / 2;
			case 3:return THREE;
			case 4:return BLOCK_FOUR;
			case 5:return FOUR;
			}
		}
		else if (block == 1) {
			switch (count) {
			case 2:return BLOCK_TWO;
			case 3:return BLOCK_THREE;
			case 4:return BLOCK_FOUR;
			case 5:
				if ((block_l && empty == count - 1) || (block_r && empty == 1)) {
					return FOUR;
				}
				return BLOCK_FOUR;
			}
		}
		else if (block == 2) {
			if (count >= 4) {
				return BLOCK_FOUR;
			}
		}
	}
	else if (empty == 2 || empty == count - 2) {
		if (count >= 7) {
			return FIVE;
		}
		if (block == 0) {
			switch (count) {
			case 3:return THREE;
			case 4:
			case 5:return BLOCK_FOUR;
			case 6:return FOUR;
			}
		}
		else if (block == 1) {
			switch (count) {
			case 3:return BLOCK_THREE;
			case 4:
			case 5:return BLOCK_FOUR;
			case 6:
				if ((block_l && empty == count - 2) || (block_r && empty == 2)) {
					return FOUR;
				}
				return BLOCK_FOUR;
			}
		}
		else if (block == 2) {
			if (count >= 4) {
				return BLOCK_FOUR;
			}
		}
	}
	else if (empty == 3 || empty == count - 3) {
		if (count >= 8) {
			return FIVE;
		}
		if (block == 0) {
			switch (count) {
			case 4:
			case 5:
			case 6:return BLOCK_FOUR;
			case 7:return FOUR;
			}
		}
		else if (block == 1) {
			switch (count) {
			case 4:
			case 5:
			case 6:return BLOCK_FOUR;
			case 7:
				if ((block_l && empty == count - 3) || (block_r && empty == 3)) {
					return FOUR;
				}
				return BLOCK_FOUR;
			}
		}
		else if (block == 2) {
			if (count >= 4) {
				return BLOCK_FOUR;
			}
		}
	}
	else if (empty == 4 || empty == count - 4) {
		if (count >= 9) {
			return FIVE;
		}
		if (block == 0) {
			if (count >= 5) {
				return FOUR;
			}
		}
		else if (block == 1) {
			if (count >= 5 && count <= 7) {
				if ((block_l && empty == count - 4) || (block_r && empty == 4)) {
					return BLOCK_FOUR;
				}
			}
			return FOUR;
		}
		else if (block == 2) {
			if (count >= 5) {
				return BLOCK_FOUR;
			}
		}
	}
	else if (empty == 5 || empty == count - 5) {
		return FIVE;
	}
	return 0;
}

void chessboard::value_change_after_draw(int i, int j) {
	int color = get_the_color(i, j);
	one_point_value_update(i, j, -1);
	int count = 0;
	int i_t, j_t;
	bool isIn = false;
	for (int c = 0; c < 4; c++) {
		isIn = false;
		for (int m = -RADIUS; m < RADIUS + 1; m++) {
			if (m == 0) continue;
			i_t = i + m * dir[c][0];
			j_t = j + m * dir[c][1];
			if (isInBoard(i_t, j_t)) {
				isIn = true;
				one_point_value_update(i_t, j_t, count);
			}
			else {
				if (isIn) break;
				continue;

			}
		}
		count++;
	}

}
void chessboard::one_point_value_update(int i, int j, int dir_idx) {
	int color = get_the_color(i, j);
	if (dir_idx == -1) {
		int* value;
		switch (color) {
		case BLACK:
			value = one_point_value(i, j, BLACK, -1);
			for (int g = 0; g < 4; g++) {
				black_value_idx[i][j][g] = value[g];
				white_value_idx[i][j][g] = 0;
			}
			break;
		case WHITE:
			value = one_point_value(i, j, WHITE, -1);
			for (int g = 0; g < 4; g++) {
				white_value_idx[i][j][g] = value[g];
				black_value_idx[i][j][g] = 0;
			}
			break;
		case EMPTY:
			int* value1 = one_point_value(i, j, BLACK, -1);
			int* value2 = one_point_value(i, j, WHITE, -1);
			for (int g = 0; g < 4; g++) {
				white_value_idx[i][j][g] = value2[g];
				black_value_idx[i][j][g] = value1[g];
			}
			break;
		}

	}
	else {
		int value = 0;
		switch (color) {
		case BLACK:
			value = one_point_value_one_dir(i, j, BLACK, dir_idx);

			black_value_idx[i][j][dir_idx] = value;
			white_value_idx[i][j][dir_idx] = 0;
			break;
		case WHITE:
			value = one_point_value_one_dir(i, j, WHITE, dir_idx);

			white_value_idx[i][j][dir_idx] = value;
			black_value_idx[i][j][dir_idx] = 0;
			break;
		case EMPTY:
			int value1 = one_point_value_one_dir(i, j, BLACK, dir_idx);
			int value2 = one_point_value_one_dir(i, j, WHITE, dir_idx);
			black_value_idx[i][j][dir_idx] = value1;
			white_value_idx[i][j][dir_idx] = value2;
			break;
		}
	}
	int tmp1 = 0;
	int tmp2 = 0;
	for (int c = 0; c < 4; c++) {
		tmp1 += black_value_idx[i][j][c];
		tmp2 += white_value_idx[i][j][c];
	}
	black_value[i][j] = tmp1;
	white_value[i][j] = tmp2;

}


int chessboard::value_judge_best(int color) {
	int tmp1 = 0;
	int tmp2 = 0;
	for (int i = 0; i < 15; i++) {
		for (int j = 0; j < 15; j++) {
			if (get_the_color(i, j) == BLACK) {
				tmp1 += score_polish(black_value[i][j]);
			}
			else if (get_the_color(i, j) == WHITE) {
				tmp2 += score_polish(white_value[i][j]);
			}
		}
	}
	if (color == BLACK) {
		return tmp1 - tmp2;
	}
	else if (color == WHITE) {
		return tmp2 - tmp1;
	}
	return 0;

}

int chessboard::score_polish(int score) {
	if (score < FOUR && score >= BLOCK_FOUR) {
		if (score >= BLOCK_FOUR && score < BLOCK_FOUR + THREE) {
			return THREE;
		}
		else if (score >= BLOCK_FOUR + THREE && score < 2 * BLOCK_FOUR) {
			return FOUR;
		}
		else {
			return FOUR * 2;
		}
	}
	if (score < BLOCK_FOUR && score >= 2 * THREE) {
		return 5 * BLOCK_FOUR;
	}
	return score;
}
UI_board chessboard::showBoard(){
    UI_board retBoard;
    for(int i = 0;i < 15;i ++){
        for(int j = 0;j < 15;j ++){
            retBoard.item[i][j] = board[i][j];
        }
    }
    return retBoard;
}
