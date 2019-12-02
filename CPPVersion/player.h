#ifndef PLAYER_H
#define PLAYER_H

#define STUPID 2
#define EASY 4
#define GOOD 6
#define MASTER 8
#define GOD 10

#include"chessboard.h"
#include"AI.h"

// the class to manage player
class player{
public:
    int my_color;
    virtual ~player(){}
    virtual int* Go(chessboard board){}
};


class humanPlayer: public player{
public:
    humanPlayer(int color);
    int* Go(chessboard board);
};

class AIPlayer:public player{
public:
    AIPlayer(int color,int difficulty);
    int* Go(chessboard board);
private:
    int my_depth;
    AI *ai;
};

#endif // PLAYER_H
