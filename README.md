# World Cup Simulator

This project is a complete Python-based simulation of the FIFA World Cup tournament. It runs the entire competition, from the group stage to the final knockout match, and calculates the probability of each team winning the championship. The simulation is driven by a structured dataset, and every time you run the program, it instantly produces a visual chart showing the title chances for all participating teams.

The architecture is fully modular, making the code clean, maintainable, and easy to understand. The logic is separated into five distinct classes, each handling a specific part of the tournament:

- Team: Manages individual team attributes, strength ratings, and performance metrics.
- GroupStage: Handles group draws, match scheduling, point calculations, and ranking to determine which teams advance.
- KnockoutStage: Generates the bracket tree and simulates single-elimination matches up to the final.
- Tournament: Oversees the overall flow of the event by combining the group and knockout phases.
- WorldCupSimulator: Serves as the main engine that initializes all components, runs the simulation loops, and gathers the final statistics.

The only file you need to execute is `main.py`. This is the entry point of the application. Before running it, make sure that the required CSV data file is placed in the exact same directory as `main.py`. The program depends on this file to load team information and will not start without it.

To get the simulation up and running, you need to install a couple of Python libraries. Open your terminal and run the following command:

pip install pandas matplotlib

Once the dependencies are installed, navigate to your project folder and start the simulator with this simple command:

python main.py

As soon as the execution finishes, the program will automatically generate and display an image file containing a clear bar chart or pie chart. This visualization shows the championship probability for every team, giving you an instant and engaging overview of the most likely winner based on the current data.

Feel free to modify the CSV file to update team stats, add new squads, or tweak performance numbers. Each time you change the data and rerun the script, you will get a fresh set of results and a new chart. This makes the simulator a great tool for football fans, data enthusiasts, or anyone curious to see how different team strengths affect the outcome of the world's biggest sporting event.

Simply place your CSV file next to main.py, run the script, and enjoy discovering which nation takes the trophy home.
