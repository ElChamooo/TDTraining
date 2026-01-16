# Visual Maze Generator

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
- [Usage](#usage)
    - [Running the Game](#running-the-game)
    - [Running Tests](#running-tests)
- [Game Mechanics](#game-mechanics)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Introduction
This project is an educational Python application using Pygame to visualize procedural maze generation algorithms commonly used in video games. It allows users to generate mazes in real-time, explore them manually, and understand the step-by-step process of creating dynamic environments. Unlike a full game, it's a tool for learning about algorithms like random generation and corridor-based mazes.

## Features
- **Procedural Maze Generation**: Supports multiple algorithms, including default random generation and corridor-based mazes.
- **Real-Time Visualization**: Watch mazes build step-by-step with Pygame interface.
- **Interactive Exploration**: Move through generated mazes using keyboard controls.
- **Debug Mode**: Regenerate mazes on-the-fly for testing.
- **Configurable Parameters**: Adjust maze size and settings via JSON file.
- **Unit Tests**: Comprehensive test suite for cells, mazes, and performance.
- **Modular Architecture**: Easy to extend with new generation algorithms or features.

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Virtual environment (recommended)
- Git (for cloning the repository)

### Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd TDTraining
   ```
2. Create and activate a virtual environment:
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```
   pip install pygame pytest
   ```

## Usage

### Running the Game
From the root directory, run:
```
python3 src/app.py
```
Add `--debug` for debug mode (regenerate with 'R' key).

Once launched:
- Use buttons to generate mazes.
- Use arrow keys to move through the maze.
- Close the window to quit.

### Running Tests
Run all tests:
```
python3 -m pytest src/tests/
```
Run a specific test file:
```
python3 -m pytest src/tests/test_cell.py -v
```

## Game Mechanics
- **Maze Structure**: Mazes are grids of cells with walls, free spaces, and special markers (start, end).
- **Generation Algorithms**: 
  - `GenRandomDefault`: Basic random maze creation.
  - `GenRandomCorridors`: Corridor-based generation for more complex layouts.
- **Exploration**: Manual movement with collision detection.
- **States**: Generating, Playing, Resolving (resolving mode not yet implemented).

## Contributing
Contributions are welcome! Please submit issues or pull requests on GitHub. Follow standard Python coding practices and add tests for new features.

## License
This project is licensed under the MIT License.

## Acknowledgments
Built with Pygame for graphics and user interface. Inspired by procedural generation techniques in game development.