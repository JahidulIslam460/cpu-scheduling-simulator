"""Reproduce the interactive, batch, and starvation/aging experiments."""
import csv
from pathlib import Path
from main import Process, fcfs, sjf, srtf, round_robin, priority_scheduling

OUT = Path(__file__).resolve().parent / "experimental_results.csv"

workloads = {
    "Interactive": [Process("I1",0,2,2), Process("I2",1,1,1),
                    Process("I3",2,2,2), Process("I4",3,1,1)],
    "Batch": [Process("B1",0,10,2), Process("B2",1,8,1),
              Process("B3",2,6,3), Process("B4",3,4,2)],
}
algorithms = [
    ("FCFS", lambda p: fcfs(p)),
    ("SJF", lambda p: sjf(p)),
    ("SRTF", lambda p: srtf(p)),
    ("RR q=2", lambda p: round_robin(p, 2)),
    ("Priority + Aging", lambda p: priority_scheduling(p, 4)),
]
rows = []
for workload, jobs in workloads.items():
    for name, run in algorithms:
        result = run(jobs)
        rows.append({
            "workload": workload, "algorithm": name,
            "avg_waiting": round(result["averages"]["waiting"], 2),
            "avg_turnaround": round(result["averages"]["turnaround"], 2),
            "avg_response": round(result["averages"]["response"], 2),
            "throughput": round(result["throughput"], 3),
            "cpu_utilization_percent": round(result["cpu_utilization"], 1),
            "gantt": " ".join(f'{s["pid"]}:{s["start"]}-{s["end"]}' for s in result["gantt"])
        })
with OUT.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
print(f"Wrote {OUT}")
