#include "game.h"
#include <iostream>
#include<windows.h>
//game::game(QObject* par):QThread(par)
//{
//    //qDebug() << "game thread:" << QThread::currentThreadId();
//    board = chessboard();
//    isPlayersReady = false;

//}

void game::reStartSet()
{
    board.clear();
    toGo = BLACK;
}

//void game::reStart(){
//    board.clear();
//    toGo = BLACK;
//    gameRun();
//}
void game::playersReady(int blackType,int whiteType){
    if(blackType <0 || blackType>5 || whiteType <0 || whiteType > 5){
        return;
    }
    switch(blackType){
    case 0:black = new humanPlayer(BLACK);break;
    case 1:black = new AIPlayer(BLACK,2);break;
    case 2:black = new AIPlayer(BLACK,4);break;
    case 3:black = new AIPlayer(BLACK,6);break;
    case 4:black = new AIPlayer(BLACK,8);break;
    case 5:black = new AIPlayer(BLACK,10);break;
    }
    switch(whiteType){
    case 0:white = new humanPlayer(WHITE);break;
    case 1:white = new AIPlayer(WHITE,2);break;
    case 2:white = new AIPlayer(WHITE,4);break;
    case 3:white = new AIPlayer(WHITE,6);break;
    case 4:white = new AIPlayer(WHITE,8);break;
    case 5:white = new AIPlayer(WHITE,10);break;
    }
}

bool game::isGamePlayerReady(){
    return isPlayersReady;
}

UI_board game::getBoard(){
    UI_board retBoard = board.showBoard();
    return retBoard;
}


int* game::gameRun(){

    int *go = new int[2];
    int *rel = new int[3];
    if(toGo == BLACK){
        go = black->Go(board);
    }
    if(toGo == WHITE){
        go = white->Go(board);
    }

    board.draw(go[0],go[1],toGo);
    int winner = board.anyone_win(go[0],go[1]);
    toGo = toGo % 2 + 1;
    rel[0] = go[0];
    rel[1] = go[1];
    rel[2] = winner;
    return rel;
}

void game::run()
{
    reStartSet();
    int *rel = new int[3];
    mouse_xy[0] = -1;
    mouse_xy[1] = -1;
    while(1){

        rel = gameRun();

        emit resultReady(rel);
        if(rel[2] != EMPTY)
            return;
    }
}
