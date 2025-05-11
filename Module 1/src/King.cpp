// king.cpp
#include "../include/king.h"
#include <cmath>

King::King(char color) : Piece(color, 'K') {}

bool King::isValidMove(int srcRow, int srcCol, int dstRow, int dstCol,
                       const std::vector<std::vector<Piece*>>& board) const {
    // King moves one square in any direction (vertically, horizontally, or diagonally)
    return std::abs(srcRow - dstRow) <= 1 && std::abs(srcCol - dstCol) <= 1;
}
