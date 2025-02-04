# SEIR Epidemic Simulation with Real-Time Visualization

## Overview
This project simulates the dynamics of an epidemic using the SEIR (Susceptible-Exposed-Infected-Recovered) model. The simulation combines:

- **Pygame**: For real-time animation of individuals moving and interacting.
- **Matplotlib**: For live-updating plots that visualize epidemic curves over time.

The simulation allows you to explore how parameters like vaccination rates, infection radius, and incubation periods affect the progression of an outbreak.

## Features
- Real-time visualization of individuals transitioning between SEIR states.
- Adjustable parameters to simulate various epidemic scenarios.
- Integration of vaccination effects on disease spread.
- Simultaneous live plotting of SEIR curves using Matplotlib.

## Requirements
Ensure you have the following installed:

- Python 3.8+
- Pygame
- Matplotlib
- FFmpeg (optional, for creating GIFs from the simulation)

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/MaximeJabarian/covid_simulation.git
   cd covid_simulation
   ```

2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the main simulation script:
   ```bash
   python covid_simulation.py
   ```

2. Adjust parameters in the `covid_simulation.py` file to explore different scenarios:
   - **Population size (N)**
   - **Infection radius**
   - **Vaccination rate**
   - **Incubation and infectious periods**

3. Watch the Pygame window for the animation and the Matplotlib window for live plots.


## Contributing
Feel free to fork this repository and make improvements. Pull requests are welcome!

## License
This project is open source.
