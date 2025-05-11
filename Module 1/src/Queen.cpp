// queen.cpp
#include "../include/queen.h"
#include <cmath>

Queen::Queen(char color) : Piece(color, 'Q') {}

bool Queen::isValidMove(int srcRow, int srcCol, int dstRow, int dstCol,
                        const std::vector<std::vector<Piece*>>& board) const {
    if (srcRow == dstRow || srcCol == dstCol || abs(dstRow - srcRow) == abs(dstCol - srcCol)) {
        return isPathClear(srcRow, srcCol, dstRow, dstCol, board);
    }
    return false;
}
    