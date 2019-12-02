#include<ctime>
#include <iostream>
#include<cstring>

#include"const.h"
#include"chessboard.h"
#include"AI.h"
#include"tools.h"

using namespace std;


int test_gobang() {
	//chessboard(int board_tmp[15][15], int black_value_idx_tmp[15][15][4], int white_value_idx_tmp[15][15][4])
	int board_tmp[15][15];
	int black_value_idx_tmp[15][15][4];
	int white_value_idx_tmp[15][15][4];

	for (int i = 0; i < 15; i++) {
		for (int j = 0; j < 15; j++) {
			board_tmp[i][j] = 0;
			for (int c = 0; c < 4; c++) {
				black_value_idx_tmp[i][j][c] = 0;
				white_value_idx_tmp[i][j][c] = 0;
			}
		}
	}
	chessboard board = chessboard(board_tmp,black_value_idx_tmp,white_value_idx_tmp);
	//AI ai1 = AI(true,8,2);
	//AI ai2 = AI(false,2);
	int* move1 = new int[2];
	int* move2 = new int[2];

	int iii;
	int jjj;
	time_t start = time(0);
	time_t end1 = time(0);
	time_t end2 = time(0);
	
	
	int params[13][2] = { {2,-1},{4,-1},{2,10},{4,10},{6,10},{7,10},{2,5},{4,5},{6,5},{8,5},{2,7},{4,7},{6,7} };
	int winner;
	int count = 0;
	AI ai1 = AI(true, 7,10);
	AI ai2 = AI(false, 7, 10);
	//for (int m = 0; m < 13; m++) {
	//	for (int n = 0; n < 13; n++) {
	//		count++;
	//		ai1.set(params[m][0], params[m][1]);
	//		ai2.set(params[n][0], params[n][1]);
	//		board.clear();
	//		for (int i = 0; i < 225; i++) {
	//			move1 = ai1.get_move(board);
	//			board.draw(move1[0], move1[1], BLACK);

	//			winner = board.anyone_win(move1[0], move1[1]);

	//			if (winner != EMPTY) {
	//				cout << "Squ: " << count << " And winner is :" << winner << endl;
	//				cout << "BlackPlayer: depth: " << params[m][0] << " cut: " << params[m][1] << endl;
	//				cout << "WhitePlayer: depth: " << params[n][0] << " cut: " << params[n][1] << endl;
	//				cout << "**********************************************************" << endl;
	//				cout << endl;
	//				break;
	//			}

	//			move2 = ai2.get_move(board);

	//			board.draw(move2[0], move2[1], WHITE);

	//			winner = board.anyone_win(move2[0], move2[1]);
	//			if (winner != EMPTY) {
	//				cout << "Squ: " << count << " And winner is :" << winner << endl;
	//				cout << "BlackPlayer: depth: " << params[m][0] << " cut: " << params[m][1] << endl;
	//				cout << "WhitePlayer: depth: " << params[n][0] << " cut: " << params[n][1] << endl;
	//				cout << "**********************************************************" << endl;
	//				cout << endl;
	//				break;
	//			}
	//			//print_board(board);
	//			

	//		}



	//	}
	//}
	
	for (int i = 0; i < 300; i++) {
		start = time(0);
		move1 = ai1.get_move(board);

		
		board.draw(move1[0], move1[1], BLACK);
		cout << "Black" << move1[0] << "," << move1[1] << endl;
		cout << board.value_judge_best(BLACK) << endl;
		end1 = time(0);
		cout << "Black Time cost: " << end1 - start << endl;
		iii = move1[0];
		jjj = move1[1];
		print_board(board);
		
		if (board.anyone_win(iii, jjj) != EMPTY) {
			cout << "winner get!" << endl;
			break;
		}
		
		//cin.get();
		start = time(0);
		//move2 = ai2.get_move(board);
		
		cin >> iii >> jjj;
		move2[0] = iii;
		move2[1] = jjj;
		board.draw(move2[0], move2[1], WHITE);
		cout << "White" << move2[0] << "," << move2[1] << endl;
		cout << board.value_judge_best(BLACK) << endl;
		
		end2 = time(0);
		cout << "White Time cost: " << end2 - start << endl;
		
		print_board(board);
		iii = move2[0];
		jjj = move2[1];
		if (board.anyone_win(iii, jjj) != EMPTY) {
			cout << "winner get!" << endl;
			break;
		}
		//cin.get();
		
	}
	cin.get();

	

}

//int* move;
//chessboard board = chessboard(a, b, c, d, e);
//AI ai = AI(j, k, l);
//move = ai.get_move(board);
//
//cout << move[0] << move[1] << endl;
//print_board(board);
//cout << move[0] << move[1] << endl;