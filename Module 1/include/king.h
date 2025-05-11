// king.h
#pragma once
#include "piece.h"

class King : public Piece {
public:
    King(char color);
    bool isValidMove(int srcRow, int srcCol, int dstRow, int dstCol,
                     const std::vector<std::vector<Piece*>>& board) const override;
};
