// game.h
#pragma once
#include "board.h"
#include <map>

class Game {
public:
    Game();
    void play();

private:
    Board board_;
    char currentTurn_;    // 'W' or 'B'
    bool isGameOver_;
    std::map<char,int> score_{{'W',0},{'B',0}};

    void initializeBoard();
    bool isValidMove(int srcR, int srcC, int dstR, int dstC) const;
    bool isInCheck(char player) const;
    bool hasAnyLegalMove(char player) const;
    bool checkCheckmate(char player) const;
    void switchTurn();
    bool makeMove(int srcR, int srcC, int dstR, int dstC);
    bool wouldBeInCheck(char player, int srcR, int srcC, int dstR, int dstC) const;
};
