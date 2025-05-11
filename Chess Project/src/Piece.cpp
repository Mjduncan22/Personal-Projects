// piece.cpp
#include "../include/piece.h"
#include <cmath>

Piece::Piece(char color, char symbol) : color_(color), symbol_(symbol) {}

Piece::~Piece() {}

char Piece::getColor() const {
    return color_;
}

char Piece::getSymbol() const {
    return symbol_;
}
bool Piece::isPathClear(int srcRow, int srcCol,
                        int dstRow, int dstCol,
                        const std::vector<std::vector<Piece*>>& board) const {
    int dRow = (dstRow - srcRow) == 0
               ? 0
               : (dstRow - srcRow) / std::abs(dstRow - srcRow);
    int dCol = (dstCol - srcCol) == 0
               ? 0
               : (dstCol - srcCol) / std::abs(dstCol - srcCol);

    int r = srcRow + dRow;
    int c = srcCol + dCol;

    while (r != dstRow || c != dstCol) {
        if (board[r][c] != nullptr) return false;
        r += dRow;
        c += dCol;
    }
    return true;
}

