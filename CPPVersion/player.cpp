#include "player.h"
#include "const.h"
#include<ctime>
#include<iostream>
#include<windows.h>
AIPlayer::AIPlayer(int color,int difficulty = 6){
    my_color = color;
    my_depth = difficulty;
    bool is_black = true;
    if(color == BLACK) is_black = true;
    if(color == WHITE) is_black = false;
    ai = new AI(is_black,my_depth,10);

}
int* AIPlayer::Go(chessboard board){
    return ai->get_move(board);
}

humanPlayer::humanPlayer(int color){
    my_color = color;
}
int* humanPlayer::Go(chessboard board){
    double on_x = 0;
    double on_y = 0;
    int* chess_point = new int[2];
    while(1){
        Sleep(300);
        if(mouse_xy[0] >= 0){

            on_x = mouse_xy[0] - 7;
            on_y = mouse_xy[1]  - 25;
            mouse_xy[0] = -1;
            mouse_xy[1] = -1;

            chess_point[0] = int((on_x + 18.2 - 20) / 36.4);
            chess_point[1] = int((on_y + 18.2 - 20) / 36.4);
            if(chess_point[0] >= 14) chess_point[0] = 14;
            if(chess_point[0] <= 0) chess_point[0] = 0;
            if(chess_point[1] >= 14) chess_point[1] = 14;
            if(chess_point[1] <= 0) chess_point[1] = 0;
            if(board.get_the_color(chess_point[0],chess_point[1]) == EMPTY)
                return chess_point;
            else
                continue;
        }
    }
}

