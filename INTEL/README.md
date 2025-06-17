# Smart AI Job-Shop Scheduler for SMEs

An AI-powered job-shop scheduling system that optimizes task allocation and machine utilization for small and medium-sized enterprises (SMEs).

## Features

- 📊 Interactive web interface using Streamlit
- ⚡ Constraint Programming-based optimization using Google OR-Tools
- 📈 Visual analytics with Gantt charts and utilization metrics
- 📁 CSV-based data input for easy integration
- 🎯 Makespan optimization
- 📊 Machine utilization analysis

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd smart-job-shop-scheduler
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run app/app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Upload your job data in CSV format with the following columns:
   - JobID: Unique identifier for each job
   - TaskID: Task number within the job
   - MachineID: Machine identifier (e.g., M1, M2, M3)
   - Duration: Time required for the task

4. Click "Run Optimizer" to generate the optimal schedule

5. View the results:
   - Gantt chart showing the optimized schedule
   - Machine utilization analysis
   - Detailed schedule table

## Sample Data

A sample CSV file is provided in the `data` directory. The format is:

```csv
JobID,TaskID,MachineID,Duration
1,1,M1,3
1,2,M2,2
1,3,M3,4
...
```

## Project Structure

```
smart-job-shop-scheduler/
├── app/
│   └── app.py              # Streamlit web interface
├── data/
│   └── jobs.csv           # Sample job data
├── scheduler/
│   └── scheduler.py       # Core scheduling logic
├── visualization/
│   └── visualizer.py      # Visualization utilities
├── requirements.txt       # Project dependencies
└── README.md             # Project documentation
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 