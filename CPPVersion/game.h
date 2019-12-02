#ifndef GAME_H
#define GAME_H
#include"chessboard.h"
#include"AI.h"
#include"player.h"
#include <QThread>
#include <QDebug>
class game : public QThread
{
    Q_OBJECT

public:
    chessboard board;

    player *black;
    player *white;
    bool exit = false;
    int toGo = BLACK;



    game(QObject* par = nullptr):QThread(par){
        qDebug() << "Thread:" << QThread::currentThreadId();
        board = chessboard();
        isPlayersReady = false;
    }
    //virtual ~game(){}
    void reStartSet();
    UI_board getBoard();
    void playersReady(int blackType,int whiteType);
    bool isGamePlayerReady();
    int* gameRun();

protected:
    void run();
signals:
    void resultReady(int *value);
private:
    bool isPlayersReady = false;


};

#endif // GAME_H
