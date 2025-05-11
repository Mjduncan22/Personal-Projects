// queen.h
#pragma once
#include "piece.h"

class Queen : public Piece {
public:
    Queen(char color);
    bool isValidMove(int srcRow, int srcCol, int dstRow, int dstCol,
                     const std::vector<std::vector<Piece*>>& board) const override;
};
