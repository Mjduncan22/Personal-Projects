// Game.cpp

#include "../include/game.h"
#include <iostream>
#include <string>

Game::Game()
  : board_()
  , currentTurn_('W')
  , isGameOver_(false)
{
    initializeBoard();
}

void Game::initializeBoard() {
    board_.initialize();
}

void Game::play() {
    while (!isGameOver_) {
        board_.display();
        std::cout << "Player " << currentTurn_
                  << "'s turn. Enter move (e.g. 2 e 4 e) or 'quit': ";

        std::string srcRowStr, dstRowStr;
        char srcColChar, dstColChar;
        std::cin >> srcRowStr;
        if (!std::cin || srcRowStr == "quit") {
            std::cout << "Quitting the game. Goodbye!\n";
            break;
        }
        std::cin >> srcColChar >> dstRowStr >> dstColChar;

        int sr = std::stoi(srcRowStr) - 1;
        int sc = srcColChar - 'a';
        int dr = std::stoi(dstRowStr) - 1;
        int dc = dstColChar - 'a';

        // 1) Validate selection
        Piece* p = board_.getPiece(sr, sc);
        if (!p || p->getColor() != currentTurn_) {
            std::cout << "Invalid selection. Try again.\n\n";
            continue;
        }
        // 2) Validate move legality
        if (!isValidMove(sr, sc, dr, dc)) {
            std::cout << "Illegal move for that piece.\n\n";
            continue;
        }
        // 3) Validate that *you* don't remain in check
        if (wouldBeInCheck(currentTurn_, sr, sc, dr, dc)) {
            std::cout << "Move would leave you in check.\n\n";
            continue;
        }

        // 4) Perform the move (including scoring)
        makeMove(sr, sc, dr, dc);

        // Determine the opponent
        char opponent = (currentTurn_ == 'W' ? 'B' : 'W');

        // 5) Check for check on opponent
        if (isInCheck(opponent)) {
            std::cout << "Check on "
                      << (opponent == 'W' ? "White" : "Black")
                      << "!\n";
        }

        // 6) Checkmate on opponent
        if (checkCheckmate(opponent)) {
            board_.display();
            std::cout << "Checkmate! Player "
                      << (currentTurn_ == 'W' ? "White" : "Black")
                      << " wins.\n";
            isGameOver_ = true;
            break;
        }

        // 7) All clear—switch turns
        switchTurn();
        std::cout << "\n";
    }
}
// Function to check if a move is valid. Based on the method of the piece type.
bool Game::isValidMove(int srcR, int srcC, int dstR, int dstC) const {
    Piece* p = board_.getPiece(srcR, srcC);
    if (!p || p->getColor() != currentTurn_) return false;
    return p->isValidMove(srcR, srcC, dstR, dstC, board_.getBoardVector());
}

// Simulate the move and check if it would leave the player in check.
bool Game::wouldBeInCheck(char player, int srcR, int srcC, int dstR, int dstC) const {
    // temporarily mutate board
    auto& grid = const_cast<Board&>(board_).getGrid();
    Piece* moving  = grid[srcR][srcC];
    Piece* captured = grid[dstR][dstC];

    grid[dstR][dstC] = moving;
    grid[srcR][srcC] = nullptr;
    bool inCheck = isInCheck(player);

    // restore original state
    grid[srcR][srcC] = moving;
    grid[dstR][dstC] = captured;
    return inCheck;
}

// Check if the player is in check. This is done by finding the king and
// checking if any enemy piece can attack it.
// This is a constant method, as it does not modify the game state.
bool Game::isInCheck(char player) const {
    int kR = -1, kC = -1;
    // find the king
    for (int r = 0; r < 8; ++r) {
        for (int c = 0; c < 8; ++c) {
            Piece* p = board_.getPiece(r, c);
            if (p && p->getColor() == player && p->getSymbol() == 'K') {
                kR = r;
                kC = c;
            }
        }
    }
    if (kR < 0) return false;

    // see if any enemy piece can attack the king
    for (int r = 0; r < 8; ++r) {
        for (int c = 0; c < 8; ++c) {
            Piece* p = board_.getPiece(r, c);
            if (p && p->getColor() != player) {
                if (p->isValidMove(r, c, kR, kC, board_.getBoardVector()))
                    return true;
            }
        }
    }
    return false;
}

// Check if the player has any legal moves. This is done by checking if
// any piece of the player can move to a valid position without leaving
// the player in check.
bool Game::hasAnyLegalMove(char player) const {
    for (int r = 0; r < 8; ++r) {
        for (int c = 0; c < 8; ++c) {
            Piece* p = board_.getPiece(r, c);
            if (!p || p->getColor() != player) continue;

            for (int dr = 0; dr < 8; ++dr) {
                for (int dc = 0; dc < 8; ++dc) {
                    // check movement pattern
                    if (!p->isValidMove(r, c, dr, dc, board_.getBoardVector()))
                        continue;
                    // check that move doesn't leave in check
                    if (wouldBeInCheck(player, r, c, dr, dc))
                        continue;
                    // found a safe move
                    return true;
                }
            }
        }
    }
    return false;
}

// Check if the player is in checkmate. This is done by checking if the
// player is in check and has no legal moves.
bool Game::checkCheckmate(char player) const {
    return isInCheck(player) && !hasAnyLegalMove(player);
}

// Function to switch the turn to the other player
void Game::switchTurn() {
    currentTurn_ = (currentTurn_ == 'W' ? 'B' : 'W');
}

// Function to make a move on the board
bool Game::makeMove(int srcR, int srcC, int dstR, int dstC) {
    Piece* cap = board_.getPiece(dstR, dstC);
    bool ok = board_.movePiece(srcR, srcC, dstR, dstC);
    if (ok && cap) {
        static const std::map<char,int> vals {
            {'P', 1}, {'N', 3}, {'B', 3},
            {'R', 5}, {'Q', 9}, {'K', 100}
        };
        char sym = std::toupper(static_cast<unsigned char>(cap->getSymbol()));
        auto it = vals.find(sym);
        if (it != vals.end()) {
            score_[currentTurn_] += it->second;
        }
    }
    return ok;
}
