#pragma once
#include"chessboard.h"

using namespace std;



void print_step(int color) {
	if (color == EMPTY) {
		cout << "_";
	}
	if (color == BLACK) {
		cout << "O";
	}
	if (color == WHITE) {
		cout << "X";
	}
}
void print_board(chessboard board) {
	for (int i = -1; i < 15; i++) {
		for (int j = -1; j < 15; j++) {
			if (i == -1 && j == -1) {
				cout << "\t";
				continue;
			}
			if (i == -1) {
				cout << j << " ";
				continue;
			}
			if (j == -1) {
				cout << i << "\t";
				continue;
			}

			cout << " ";
			print_step(board.board[i][j]);
		}
		cout << endl;
	}
}