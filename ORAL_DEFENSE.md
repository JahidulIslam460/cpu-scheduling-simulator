# Demonstration and Oral Defense Guide

## 3–5 minute demonstration
1. Run `python main.py` and identify the five scheduling algorithms.
2. Show the process table and Gantt timeline for each algorithm.
3. Explain why SRTF can preempt P1 when a shorter process arrives.
4. Change the Round Robin quantum: `python main.py --quantum 1` and `python main.py --quantum 4`.
5. Run `python -m unittest discover -s tests -v` and explain the test coverage.
6. Run `python run_experiments.py` and open `experimental_results.csv`.
7. Explain the aging experiment and why it helps prevent starvation.

## Likely viva questions
- What is the difference between waiting time and response time?
- Why is SRTF preemptive while SJF is non-preemptive?
- How does Round Robin use its time quantum?
- What is the convoy effect in FCFS?
- Why can SJF or fixed-priority scheduling starve long/low-priority jobs?
- How does aging change effective priority?
- Why can throughput be equal across algorithms in a fully CPU-bound workload?
- What limitation would you improve first? Context-switch overhead or I/O blocking are good examples.

## Important policy decisions
- Lower numeric priority means higher priority.
- Equal priorities: earlier arrival wins; PID is the final deterministic tie-breaker.
- Priority scheduling is non-preemptive.
- Round Robin arrivals during a time slice are enqueued before the expired process is re-queued.
- Time is modeled in integer units; context-switch overhead is zero.
