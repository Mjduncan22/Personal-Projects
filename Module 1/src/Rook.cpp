// rook.cpp
#include "../include/rook.h"
#include <cmath>

Rook::Rook(char color) : Piece(color, 'R') {}

bool Rook::isValidMove(int srcRow, int srcCol, int dstRow, int dstCol,
                       const std::vector<std::vector<Piece*>>& board) const {
    if (srcRow == dstRow || srcCol == dstCol) {
        return isPathClear(srcRow, srcCol, dstRow, dstCol, board);
    }
    return false;
}
