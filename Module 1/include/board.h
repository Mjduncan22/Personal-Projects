#pragma once

#include "piece.h"
#include <vector>

class Board {
public:
    Board();
    ~Board();

    void initialize();

    void display() const;

    bool movePiece(int srcRow, int srcCol, int dstRow, int dstCol);

    Piece* getPiece(int row, int col) const;

    const std::vector<std::vector<Piece*>>& getBoardVector() const;
    
    std::vector<std::vector<Piece*>>& getGrid();


private:
    std::vector<std::vector<Piece*>> board_;
    
};
