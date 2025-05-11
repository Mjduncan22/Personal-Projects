// knight.cpp
#include "../include/knight.h"
#include <cmath>

Knight::Knight(char color) : Piece(color, 'N') {}

bool Knight::isValidMove(int srcRow, int srcCol, int dstRow, int dstCol,
                         const std::vector<std::vector<Piece*>>& board) const {
    // Knight's movement (L-shape: 2 squares in one direction and 1 square in the other)
    int rowDiff = std::abs(srcRow - dstRow);
    int colDiff = std::abs(srcCol - dstCol);
    return (rowDiff == 2 && colDiff == 1) || (rowDiff == 1 && colDiff == 2);
}
