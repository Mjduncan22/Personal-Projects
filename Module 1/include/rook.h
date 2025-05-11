// rook.h
#pragma once
#include "piece.h"

class Rook : public Piece {
public:
    Rook(char color);
    bool isValidMove(int srcRow, int srcCol, int dstRow, int dstCol,
                     const std::vector<std::vector<Piece*>>& board) const override;
};
