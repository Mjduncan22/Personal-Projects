#include "../include/board.h"
#include "../include/pawn.h"
#include "../include/rook.h"
#include "../include/knight.h"
#include "../include/bishop.h"
#include "../include/queen.h"
#include "../include/king.h"
#include <iostream>


Board::Board()
  : board_(8, std::vector<Piece*>(8, nullptr))
{}

Board::~Board() {
    for (auto& row : board_)
        for (auto* p : row)
            delete p;
}

void Board::initialize() {
    // White back rank
    board_[0][0] = new Rook('W');
    board_[0][1] = new Knight('W');
    board_[0][2] = new Bishop('W');
    board_[0][3] = new Queen('W');
    board_[0][4] = new King('W');
    board_[0][5] = new Bishop('W');
    board_[0][6] = new Knight('W');
    board_[0][7] = new Rook('W');
    // White pawns
    for (int i = 0; i < 8; ++i)
        board_[1][i] = new Pawn('W');

    // Black back rank
    board_[7][0] = new Rook('B');
    board_[7][1] = new Knight('B');
    board_[7][2] = new Bishop('B');
    board_[7][3] = new Queen('B');
    board_[7][4] = new King('B');
    board_[7][5] = new Bishop('B');
    board_[7][6] = new Knight('B');
    board_[7][7] = new Rook('B');
    // Black pawns
    for (int i = 0; i < 8; ++i)
        board_[6][i] = new Pawn('B');
}

void Board::display() const {
    // Column labels
    std::cout << "  a b c d e f g h\n";

    // Print the board
    for (int row = 7; row >= 0; --row) {

        std::cout << row + 1 << " ";

        for (int col = 0; col < 8; ++col) {
            Piece* p = board_[row][col];
            if (p) {
                char sym = p->getSymbol();
                if (p->getColor() == 'W') {
                    // Bright white text
                    std::cout << "\033[1;37m" << sym << "\033[0m ";
                } else {
                    // Bright blue text
                    std::cout << "\033[1;34m" << sym << "\033[0m ";
                }
            } else {
                std::cout << ". ";
            }
        }
        std::cout << row + 1 << "\n";
    }

    std::cout << "  a b c d e f g h\n";
}

bool Board::movePiece(int srcRow, int srcCol, int dstRow, int dstCol) {
    Piece* p = board_[srcRow][srcCol];
    if (!p) return false;
    if (!p->isValidMove(srcRow, srcCol, dstRow, dstCol, board_))
        return false;
    // capture if any
    delete board_[dstRow][dstCol];
    board_[dstRow][dstCol] = p;
    board_[srcRow][srcCol] = nullptr;
    return true;
}

Piece* Board::getPiece(int row, int col) const {
    return board_[row][col];
}

// Constant method to get the board vector
const std::vector<std::vector<Piece*>>&
Board::getBoardVector() const {
    return board_;
}

// Non-constant method to get the board vector
// This method allows modification of the board vector (e.g., for testing, similuation, etc.)
std::vector<std::vector<Piece*>>&
Board::getGrid() {
    return board_;
}