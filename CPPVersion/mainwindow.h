#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "ui_mainwindow.h"
#include "game.h"
#include <QMouseEvent>
#include <QLabel>
#include <QCloseEvent>
#include<QTimer>
QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE
class chess:public QLabel{
    void enterEvent(QEvent *event){
        event->ignore();
    }
};
class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
    bool hasChoosePlayer = false;
    bool isFristRound = true;
    int blackTotalTime = 0;
    int blackStepTime = 0;
    int whiteTotalTime = 0;
    int whiteStepTime = 0;
    chess mouse_point;
    chess all_chess[225];
    chess all_chess_squ[225];
    chess lastest;
    QPixmap black;
    QPixmap white;
    int now_color = BLACK;
    //double mouse_xy[2] = {-1,-1};
    int step = 0;
    QTimer *blackTimer;
    QTimer *whiteTimer;
    int seconds = 0;
    bool is_run = false;
    double chess_xy[2] = {-1,-1};
    int chess_point[2] = {-1,-1};
    void mouse_xy_to_chess_point();
    void chess_point_to_chess_xy();
    void gameover(int color);
    bool choosePlayer();
    void restart();
    void switchPlayer(bool ifInit);




private slots:


    void on_reStart_clicked();
    void signalDeal(int *value);

    void on_choosePlayer_clicked();

    void on_closeBtn_clicked();
    void updateTimeBlack();
    void updateTimeWhite();

private:
    game *Game;
    Ui::MainWindow *ui;
    void mouseMoveEvent(QMouseEvent *event);
    void mousePressEvent(QMouseEvent *event);
    void initUI();
    void draw();
    void closeEvent(QCloseEvent *event);
;
};



#endif // MAINWINDOW_H
