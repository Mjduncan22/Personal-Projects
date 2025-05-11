// pawn.h
#pragma once
#include "piece.h"

class Pawn : public Piece {
public:
    Pawn(char color);
    bool isValidMove(int srcRow, int srcCol, int dstRow, int dstCol,
                     const std::vector<std::vector<Piece*>>& board) const override;
};