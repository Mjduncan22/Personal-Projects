// pawn.cpp
#include "../include/pawn.h"
#include <cmath>

Pawn::Pawn(char color) : Piece(color, 'P') {}

bool Pawn::isValidMove(int srcRow, int srcCol, int dstRow, int dstCol,
                       const std::vector<std::vector<Piece*>>& board) const {
    int direction = (color_ == 'W') ? 1 : -1;
    int startRow = (color_ == 'W') ? 1 : 6;

    // One step forward
    if (srcCol == dstCol && dstRow == srcRow + direction &&
        board[dstRow][dstCol] == nullptr) {
        return true;
    }

    // Two steps forward from starting position
    if (srcCol == dstCol && srcRow == startRow && dstRow == srcRow + 2 * direction &&
        board[srcRow + direction][dstCol] == nullptr && board[dstRow][dstCol] == nullptr) {
        return true;
    }

    // Diagonal capture
    if (std::abs(srcCol - dstCol) == 1 && dstRow == srcRow + direction &&
        board[dstRow][dstCol] != nullptr && board[dstRow][dstCol]->getColor() != color_) {
        return true;
    }

    return false;
}