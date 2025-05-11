# Overview

In this project, I built a console-based chess game in C++ to strengthen my understanding of modern C++ features like classes, inheritance, STL containers, and exception handling. My goal was to create a working game while learning how to write clean, reusable code.

The result is a turn-based chess engine that enforces legal moves, detects check and checkmate, and keeps score of captured pieces. Each piece type (Pawn, Knight, Bishop, Rook, Queen, King) is implemented as its own subclass, and the game loop handles input parsing, move validation, check detection, and score updates.

My purpose in writing this software was twofold:

1. **Syntax mastery** – reinforce my knowledge of C++ class hierarchies, virtual functions, and container usage.  
2. **Design practice** – apply SOLID principles in a small project to learn how to structure code for readability and future extension.

[Software Demo Video](https://youtu.be/wfurac7eVQQ)

# Development Environment

- **Operating System:** Windows 10 
- **IDE / Editor:** Visual Studio Code with the C/C++ extension  
- **Compiler:** GCC 11.2.0 (g++) / MSVC v19.30  
- **Language Standard:** C++17  
- **Libraries:**  
  - Standard Template Library (std::vector, std::map, std::string)   

# Useful Websites

- [Stack Overflow](https://stackoverflow.com)

# Future Work

- **Stalemate logic** – correct detection of stalemate scenarios and draw conditions  
- **Castling** – implement king-and-rook castling rules (king side and queen side)  
- **Point system improvements** – refine scoring to account for positional value, pawn promotion, and endgame factors  