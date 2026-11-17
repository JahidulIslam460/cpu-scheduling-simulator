# CPU Scheduling Simulator With Workload Analysis

## Project overview
A Python 3 simulator for FCFS, non-preemptive SJF, preemptive SRTF, Round Robin, and non-preemptive Priority Scheduling with optional aging.

## Requirements
- Python 3.10+
- No external dependency is required to run the simulator or tests.
- Matplotlib is optional if regenerating the supplied Gantt chart images.

## Run the simulator
```bash
python main.py
python main.py --quantum 3 --aging 5
python main.py --input tests/sample_processes.csv --quantum 2
```

## Run tests and reproduce results
```bash
python -m unittest discover -s tests -v
python run_experiments.py
```

## CSV format
```csv
pid,arrival,burst,priority
P1,0,7,2
P2,2,4,1
```

## Scheduling policies and tie rules
- FCFS: earliest arrival first; PID breaks simultaneous-arrival ties.
- SJF: shortest original burst among ready processes; then arrival and PID.
- SRTF: shortest remaining burst at each integer time boundary; then arrival and PID.
- Round Robin: FIFO ready queue; a process runs for at most the configured quantum. Arrivals during a time slice join before the expired process is re-queued.
- Priority: lower numeric value means higher priority. Ties use earlier arrival, then PID. Aging improves effective priority by one every configured waiting interval, down to priority 0.

## Metrics
- CT: completion time
- TAT = CT - AT
- WT = TAT - BT
- RT = first CPU start - AT
- Throughput = number of completed processes / elapsed time from first arrival to final completion
- CPU utilization = busy CPU time / elapsed time * 100

## Assumptions and limitations
Single CPU, integer time, positive CPU bursts, CPU-bound jobs, and no context-switch overhead or I/O blocking. Priority scheduling is non-preemptive. Aging is applied at dispatch decisions.

## Project files
- `main.py`: simulator and command-line interface
- `tests/`: automated tests and CSV test workloads
- `run_experiments.py`: reproducible experimental metrics
- `experimental_results.csv`: calculated metrics
- `evidence/`: Gantt charts and captured terminal output
- `Technical_Report.pdf`: assignment report
- `ORAL_DEFENSE.md`: demonstration and viva preparation

## GitHub submission
Create a new GitHub repository, then from this project folder run:
```bash
git init
git add .
git commit -m "Complete CPU scheduling simulator assignment"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/cpu-scheduling-simulator.git
git push -u origin main
```
Replace the URL with your actual repository URL. Do not upload virtual environments, passwords, API keys, or private files. Ensure the instructor can access the repository.
