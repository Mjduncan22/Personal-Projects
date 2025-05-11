// piece.h
#pragma once
#include <vector>

class Piece {
public:
    Piece(char color, char symbol);
    virtual ~Piece();
    
    virtual bool isValidMove(int srcRow, int srcCol, int dstRow, int dstCol,
                             const std::vector<std::vector<Piece*>>& board) const = 0;

    char getColor() const;
    char getSymbol() const;

protected:
    char color_;
    char symbol_;
    bool isPathClear(int srcRow, int srcCol, int dstRow, int dstCol,
                     const std::vector<std::vector<Piece*>>& board) const;
};
