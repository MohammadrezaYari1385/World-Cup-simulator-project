# World Cup Simulator

This project is a complete Python-based simulation of the FIFA World Cup tournament. It runs the entire competition, from the group stage to the final knockout match, and calculates the probability of each team winning the championship. The simulation is driven by a structured dataset, and every time you run the program, it instantly produces a visual chart showing the title chances for all participating teams.

The architecture is fully modular, making the code clean, maintainable, and easy to understand. The logic is separated into five distinct classes, each handling a specific part of the tournament:

- Team: Manages individual team attributes, strength ratings, and performance metrics.
- GroupStage: Handles group draws, match scheduling, point calculations, and ranking to determine which teams advance.
- KnockoutStage: Generates the bracket tree and simulates single-elimination matches up to the final.
- Tournament: Oversees the overall flow of the event by combining the group and knockout phases.
- WorldCupSimulator: Serves as the main engine that initializes all components, runs the simulation loops, and gathers the final statistics.

The only file you need to execute is `main.py`. This is the entry point of the application. Before running it, make sure that the required CSV data file is placed in the exact same directory as `main.py`. The program depends on this file to load team information and will not start without it.

To get the simulation up and running, you need to install three Python libraries: NumPy, Pandas, and Matplotlib. These provide the mathematical operations, data handling, and plotting capabilities required for the simulation and its visual output. Open your system's terminal (Command Prompt on Windows, or Terminal on macOS/Linux) – not the Python interactive shell – and run the following command:

```bash
pip install numpy pandas matplotlib
