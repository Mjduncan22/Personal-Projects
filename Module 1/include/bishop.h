// bishop.h
#pragma once
#include "piece.h"

class Bishop : public Piece {
public:
    Bishop(char color);
    bool isValidMove(int srcRow, int srcCol, int dstRow, int dstCol,
                     const std::vector<std::vector<Piece*>>& board) const override;
};