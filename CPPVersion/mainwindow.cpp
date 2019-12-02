#include "mainwindow.h"
#include "ui_mainwindow.h"
#include"const.h"
#include<QInputDialog>
#include<windows.h>
#include<QPainter>
#include<QMessageBox>


#define PIECE 35.0
using namespace std;
MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    initUI();
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::mouse_xy_to_chess_point()
{

    double on_x = mouse_xy[0] - 7;
    double on_y = mouse_xy[1]  - 25;

    chess_point[0] = int((on_x + 18.2 - 20) / 36.4);
    chess_point[1] = int((on_y + 18.2 - 20) / 36.4);
    if(chess_point[0] >= 14) chess_point[0] = 14;
    if(chess_point[0] <= 0) chess_point[0] = 0;
    if(chess_point[1] >= 14) chess_point[1] = 14;
    if(chess_point[1] <= 0) chess_point[1] = 0;
}

void MainWindow::chess_point_to_chess_xy()
{
    chess_xy[0] = chess_point[0] * 36.4 + 20 - PIECE/2;
    chess_xy[1] = chess_point[1] * 36.4 + 20 - PIECE/2;
}

void MainWindow::gameover(int color)
{
    QString winner;
    blackTimer->stop();
    whiteTimer->stop();





    if(color == BLACK){
        cout << "black win" <<endl;
        QMessageBox blackWin(QMessageBox::NoIcon,"Black win","黑方获胜");
        blackWin.setIconPixmap(black);
        blackWin.exec();
        winner = "黑方获胜";
    }
    if(color == WHITE){
        cout << "white win" << endl;
        QMessageBox whiteWin(QMessageBox::NoIcon,"White win","白方获胜");
        whiteWin.setIconPixmap(white);
        winner = "白方获胜";
        whiteWin.exec();
    }
    if(color == FULL){
        cout << "tie" << endl;
        QMessageBox tie(QMessageBox::NoIcon,"Tie","平局");
        winner = "平局";

        tie.exec();
    }
    if(color == FORCE){
        cout << "force exit" << endl;
        winner = "游戏未开始";
    }
//    QPainter tmp(ui->blackPlayerLabel);
//    tmp.setPen(Qt::blue);
//    tmp.setFont(QFont("Arial",30));
//    tmp.drawText(rect(),Qt::AlignCenter,"Hello");
//    tmp.end();
    QFont black_num("Arial",13,QFont::Bold);
    QFont white_num("Arial",13,QFont::Bold);

    for(int i = 0;i < step;i ++){
        all_chess_squ[i].setGeometry(0,0,PIECE,PIECE);
        all_chess_squ[i].setAlignment(Qt::AlignCenter | Qt::AlignCenter);
        all_chess_squ[i].setFont(QFont("Arial",13,QFont::Bold));
        all_chess_squ[i].setText(QString::number(i+1));

    }
    ui->gameProgress->setText(winner);
    lastest.setParent(nullptr);
    Game->terminate();
    Game->wait();
}

bool MainWindow::choosePlayer()
{
    bool ok = false;
    int black_type = QInputDialog::getInt(this,"The black player","Choose the Black Player\n0 for human\n1 for stupid AI\n2 for easy AI\n3 for good AI\n4 for master AI\n5 for God AI",0,0,5,1,&ok);
    if(!ok){
        return false;
    }
    ok = false;
    int white_type = QInputDialog::getInt(this,"The white player","Choose the white Player\n0 for human\n1 for stupid AI\n2 for easy AI\n3 for good AI\n4 for master AI\n5 for God AI",0,0,5,1,&ok);
    if(!ok){
        return false;
    }

    if(black_type <0 || black_type>5 || white_type <0 || white_type > 5){

        return false;
    }
    hasChoosePlayer = true;
    Game->playersReady(black_type,white_type);
    QString blackText;
    QString whiteText;
    switch(black_type){
    case 0:blackText = "human";break;
    case 1:blackText = "AI-Stupid";break;
    case 2:blackText = "AI-Easy";break;
    case 3:blackText = "AI-Good";break;
    case 4:blackText = "AI-Master";break;
    case 5:blackText = "AI-God";break;
    }
    switch(white_type){
    case 0:whiteText = "human";break;
    case 1:whiteText = "AI-Stupid";break;
    case 2:whiteText = "AI-Easy";break;
    case 3:whiteText = "AI-Good";break;
    case 4:whiteText = "AI-Master";break;
    case 5:whiteText = "AI-God";break;
    }
    ui->blackPlayerLabel->setText(blackText);
    ui->whitePlayerLabel->setText(whiteText);
    return true;

}

void MainWindow::restart()
{
    if(!hasChoosePlayer){
        bool chooseOver = choosePlayer();
        if(!chooseOver)
            return;
    }

    gameover(FORCE);
    now_color = BLACK;
    step = 0;

    //connect(Game,SIGNAL(finished()),Game,SLOT(deleteLater()));

    for(int i = 0;i < 225;i ++){
        all_chess[i].clear();
        all_chess_squ[i].clear();
    }
    ui->gameProgress->setText("游戏进行中");

    switchPlayer(true);


    Game->start();




}

void MainWindow::switchPlayer(bool ifInit = false)
{
    blackTimer->stop();
    whiteTimer->stop();
    if(ifInit){
        blackStepTime  = 0;
        whiteStepTime = 0;
        blackTotalTime = 0;
        whiteTotalTime = 0;

        ui->blackStepTimeLabel->setText(QString::number(0));
        ui->blackTotalTimeLabel->setText(QString::number(0));
        ui->whiteStepTimeLabel->setText(QString::number(0));
        ui->whiteTotalTimeLabel->setText(QString::number(0));
        ui->blackPerStepLabel->setText(QString::number(0.00));
        ui->whitePerStepLabel->setText(QString::number(0.00));


    }
    if(ifInit || now_color == WHITE){
        now_color = BLACK;
        ui->blackChessPtr->setVisible(true);
        ui->whiteChessPtr->setVisible(false);
        mouse_point.setPixmap(black);
        blackStepTime = 0;
        blackTimer->start(1000);
        if(step > 0){
            float whitePer = float(whiteTotalTime) / float((step)/2);
            ui->whitePerStepLabel->setText(QString::number(whitePer));
        }

    }
    else if(now_color == BLACK){
        now_color = WHITE;
        ui->blackChessPtr->setVisible(false);
        ui->whiteChessPtr->setVisible(true);
        mouse_point.setPixmap(white);
        whiteStepTime = 0;
        whiteTimer->start(1000);
        if(step > 0){
            float blackPer = float(blackTotalTime) / float((step+1)/2);
            ui->blackPerStepLabel->setText(QString::number(blackPer));

        }
    }
}

void MainWindow::signalDeal(int* value)
{
    chess_point[0] = value[0];
    chess_point[1] = value[1];
    draw();
    cout << value[2] << endl;
    if(value[2] != EMPTY)
        return gameover(value[2]);
}

void MainWindow::mouseMoveEvent(QMouseEvent *event)
{
    if(event->x() >= 7 && event->x() <= 550 + 7 && event->y() >= 25 && event->y() <= 550 + 25)
        mouse_point.move(event->x() - PIECE * 0.5,event->y() - PIECE * 0.5);

}

void MainWindow::mousePressEvent(QMouseEvent *event)
{
    if(event->x() >= 7 && event->x() <= 550 + 7 && event->y() >= 25 && event->y() <= 550 + 25){
        mouse_xy[0] = event->x();
        mouse_xy[1] = event->y();
    }
//    else{
//        choosePlayer();
//    }



}

void MainWindow::initUI()
{
    blackTimer = new QTimer(this);
    whiteTimer = new QTimer(this);
    connect(blackTimer,SIGNAL(timeout()),this,SLOT(updateTimeBlack()));
    connect(whiteTimer,SIGNAL(timeout()),this,SLOT(updateTimeWhite()));

//    timer->start(1000);



    Game = new game(this);
    connect(Game,SIGNAL(resultReady(int*)),this,SLOT(signalDeal(int*)));
    ui->whiteChessPtr->setVisible(false);

    QPalette num_color;
    num_color.setColor(QPalette::WindowText,Qt::white);

    for(int i = 0;i < 225;i ++){

        all_chess[i].setParent(ui->board);
        all_chess[i].setVisible(true);
        all_chess[i].setScaledContents(true);
        all_chess_squ[i].setParent(&all_chess[i]);
        all_chess_squ[i].setVisible(true);
        all_chess_squ[i].setScaledContents(true);
        if(i % 2 == 0){
            all_chess_squ[i].setPalette(num_color);
        }
    }




    QPalette board_palette;
    QPixmap board_pix = QPixmap(":/media/board.jpg");
    ui->board->setAutoFillBackground(true);
    board_pix = board_pix.scaled(ui->board->size());
    board_palette.setBrush(ui->board->backgroundRole(),QBrush(board_pix));
    ui->board->setPalette(board_palette);




    black = QPixmap(":/media/black.png");
    white = QPixmap(":/media/white.png");

    mouse_point.setParent(this);

    mouse_point.setScaledContents(true);

    mouse_point.setGeometry(270,270,PIECE,PIECE);
    mouse_point.setPixmap(black);


    ui->board->setMouseTracking(true);
    ui->centralwidget->setMouseTracking(true);
    mouse_point.setMouseTracking(true);
    mouse_point.raise();

    setMouseTracking(true);




}

void MainWindow::draw()
{
    chess_point_to_chess_xy();

    if(now_color != BLACK && now_color != WHITE){
        return;
    }
    if(now_color == BLACK)
        all_chess[step].setPixmap(black);
    if(now_color == WHITE)
        all_chess[step].setPixmap(white);
    //cout << chess_xy[0] <<"," <<chess_xy[1]<<endl;
    all_chess[step].setGeometry(chess_xy[0],chess_xy[1],PIECE,PIECE);
    //lastest.setParent(&all_chess[step]);
    QPalette num_color;
    num_color.setColor(QPalette::WindowText,Qt::red);
    lastest.setParent(&all_chess[step]);
    lastest.setScaledContents(true);
    lastest.setVisible(true);
    lastest.setPalette(num_color);
    lastest.setAlignment(Qt::AlignCenter | Qt::AlignCenter);
    lastest.setGeometry(0,0,PIECE,PIECE);
    lastest.setFont(QFont("Arial",20,QFont::Bold));
    lastest.setText(QString("X"));
    step++;

    switchPlayer();
}

void MainWindow::closeEvent(QCloseEvent *event)
{
     if(QMessageBox::question(this,"Exit","真的要退出游戏吗") == QMessageBox::Yes){
         gameover(FORCE);

         event->accept();
     }
     else{
         event->ignore();
     }
}


void MainWindow::on_reStart_clicked()
{
    restart();
}


void MainWindow::on_choosePlayer_clicked()
{
    hasChoosePlayer = false;
    restart();
}

void MainWindow::on_closeBtn_clicked()
{
    close();
}

void MainWindow::updateTimeBlack()
{
    blackStepTime ++;
    blackTotalTime ++;
    ui->blackStepTimeLabel->setText(QString::number(blackStepTime));
    ui->blackTotalTimeLabel->setText(QString::number(blackTotalTime));
}

void MainWindow::updateTimeWhite()
{
    whiteStepTime ++;
    whiteTotalTime++;
    ui->whiteStepTimeLabel->setText(QString::number(whiteStepTime));
    ui->whiteTotalTimeLabel->setText(QString::number(whiteTotalTime));
}


