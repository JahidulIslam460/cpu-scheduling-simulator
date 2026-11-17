
# CPU Scheduling Simulator With Workload Analysis

## Project Overview

A Python 3 based CPU Scheduling Simulator that implements and compares five CPU scheduling algorithms:

1. First Come First Serve (FCFS)
2. Shortest Job First (SJF) - Non-preemptive
3. Shortest Remaining Time First (SRTF) - Preemptive
4. Round Robin (RR)
5. Priority Scheduling - Non-preemptive with optional Aging

## Requirements

- Python 3.10 or later
- No external dependencies are required to run the simulator or tests.
- Matplotlib is optional for regenerating Gantt chart images.

## Run the Simulator

Run the following commands from the project directory:

```bash
python main.py
```

Run with a custom time quantum and aging interval:

```bash
python main.py --quantum 3 --aging 5
```

Run using a CSV input file:

```bash
python main.py --input tests/sample_processes.csv --quantum 2
```

## Run Tests and Experiments

Run the automated tests:

```bash
python -m unittest discover -s tests -v
```

Run the workload experiments:

```bash
python run_experiments.py
```

## CSV Input Format

The simulator accepts CSV files with the following columns:

```csv
pid,arrival,burst,priority
P1,0,7,2
P2,2,4,1
```

## Scheduling Policies and Tie-Breaking Rules

- **FCFS:** Processes are executed in arrival order. PID breaks simultaneous-arrival ties.
- **SJF:** Selects the ready process with the shortest original burst time. Arrival time and PID break ties.
- **SRTF:** Selects the process with the shortest remaining burst time at each integer time boundary. Arrival time and PID break ties.
- **Round Robin:** Uses a FIFO ready queue. Each process runs for at most the configured time quantum. Arrivals during a time slice join the queue before the expired process is re-queued.
- **Priority Scheduling:** Uses non-preemptive scheduling. A lower numeric priority value means higher priority. Arrival time and PID break ties. Aging improves effective priority by one after each configured waiting interval, down to priority 0.

## Performance Metrics

The simulator calculates the following metrics:

- **CT (Completion Time):** Time when a process finishes.
- **TAT (Turnaround Time):** CT - AT.
- **WT (Waiting Time):** TAT - BT.
- **RT (Response Time):** First CPU start time - AT.
- **Throughput:** Number of completed processes divided by elapsed time.
- **CPU Utilization:** Busy CPU time divided by elapsed time, multiplied by 100.

Where:
- AT = Arrival Time
- BT = Burst Time

## Assumptions and Limitations

- Single CPU system.
- Integer-based time units.
- Positive CPU burst times.
- CPU-bound processes.
- No context-switch overhead.
- No I/O blocking.
- Priority scheduling is non-preemptive.
- Aging is applied at dispatch decisions.

## Project Structure

```text
CPU_Scheduling_Simulator/
│
├── main.py
├── run_experiments.py
├── experimental_results.csv
├── test_results.txt
├── Technical_Report_Completed.pdf
├── ORAL_DEFENSE.md
│
├── tests/
│   ├── sample_processes.csv
│   ├── starvation_workload.csv
│   └── test_scheduler.py
│
└── evidence/
    ├── batch_gantt.png
    ├── interactive_gantt.png
    └── sample_terminal_output.txt
```

## GitHub Submission

This project is maintained in the following GitHub repository:

https://github.com/JahidulIslam460/cpu-scheduling-simulator

The repository contains the simulator source code, automated tests, experimental results, evidence, and technical report.
