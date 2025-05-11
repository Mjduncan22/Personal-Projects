// bishop.cpp
#include "../include/bishop.h"
#include <cmath>


Bishop::Bishop(char color) : Piece(color, 'B') {}

bool Bishop::isValidMove(int srcRow, int srcCol, int dstRow, int dstCol,
                         const std::vector<std::vector<Piece*>>& board) const {
    if (abs(dstRow - srcRow) == abs(dstCol - srcCol)) {
        return isPathClear(srcRow, srcCol, dstRow, dstCol, board);
    }
    return false;
}
