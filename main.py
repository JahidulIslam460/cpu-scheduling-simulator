"""
CPU Scheduling Simulator With Workload Analysis
Algorithms: FCFS, non-preemptive SJF, SRTF, Round Robin, Priority (non-preemptive)
Python 3.10+
"""

from dataclasses import dataclass
from collections import deque
from typing import List, Dict, Optional
import argparse
import csv


@dataclass
class Process:
    pid: str
    arrival: int
    burst: int
    priority: int = 0


def validate_processes(processes: List[Process]) -> None:
    if not processes:
        raise ValueError("At least one process is required.")
    seen = set()
    for p in processes:
        if not p.pid or p.pid in seen:
            raise ValueError("Process IDs must be non-empty and unique.")
        seen.add(p.pid)
        if not isinstance(p.arrival, int) or p.arrival < 0:
            raise ValueError(f"{p.pid}: arrival time must be a non-negative integer.")
        if not isinstance(p.burst, int) or p.burst <= 0:
            raise ValueError(f"{p.pid}: burst time must be a positive integer.")
        if not isinstance(p.priority, int):
            raise ValueError(f"{p.pid}: priority must be an integer.")


def add_segment(gantt, pid, start, end):
    if start == end:
        return
    if gantt and gantt[-1]["pid"] == pid and gantt[-1]["end"] == start:
        gantt[-1]["end"] = end
    else:
        gantt.append({"pid": pid, "start": start, "end": end})


def finalize(processes, gantt, first_start):
    rows = []
    for p in processes:
        completion = max(s["end"] for s in gantt if s["pid"] == p.pid)
        turnaround = completion - p.arrival
        waiting = turnaround - p.burst
        response = first_start[p.pid] - p.arrival
        rows.append({
            "pid": p.pid, "arrival": p.arrival, "burst": p.burst,
            "priority": p.priority, "completion": completion,
            "turnaround": turnaround, "waiting": waiting,
            "response": response
        })
    first_arrival = min(p.arrival for p in processes)
    finish = max(r["completion"] for r in rows)
    busy = sum(s["end"] - s["start"] for s in gantt if s["pid"] != "IDLE")
    span = finish - first_arrival
    return {
        "gantt": gantt,
        "processes": rows,
        "averages": {
            "waiting": sum(r["waiting"] for r in rows) / len(rows),
            "turnaround": sum(r["turnaround"] for r in rows) / len(rows),
            "response": sum(r["response"] for r in rows) / len(rows),
        },
        "throughput": len(processes) / span if span else 0.0,
        "cpu_utilization": (busy / span * 100) if span else 0.0,
        "makespan": span
    }


def fcfs(processes: List[Process]):
    validate_processes(processes)
    now, gantt, first = 0, [], {}
    for p in sorted(processes, key=lambda x: (x.arrival, x.pid)):
        if now < p.arrival:
            add_segment(gantt, "IDLE", now, p.arrival)
            now = p.arrival
        first[p.pid] = now
        add_segment(gantt, p.pid, now, now + p.burst)
        now += p.burst
    return finalize(processes, gantt, first)


def sjf(processes: List[Process]):
    validate_processes(processes)
    remaining = {p.pid: p.burst for p in processes}
    by_id = {p.pid: p for p in processes}
    done, now, gantt, first = set(), 0, [], {}
    while len(done) < len(processes):
        ready = [p for p in processes if p.pid not in done and p.arrival <= now]
        if not ready:
            next_arrival = min(p.arrival for p in processes if p.pid not in done)
            add_segment(gantt, "IDLE", now, next_arrival)
            now = next_arrival
            continue
        p = min(ready, key=lambda x: (x.burst, x.arrival, x.pid))
        first[p.pid] = now
        add_segment(gantt, p.pid, now, now + p.burst)
        now += p.burst
        done.add(p.pid)
    return finalize(processes, gantt, first)


def srtf(processes: List[Process]):
    validate_processes(processes)
    remaining = {p.pid: p.burst for p in processes}
    now, completed, gantt, first = 0, set(), [], {}
    while len(completed) < len(processes):
        ready = [p for p in processes if p.pid not in completed
                 and p.arrival <= now and remaining[p.pid] > 0]
        if not ready:
            next_arrival = min(p.arrival for p in processes if p.pid not in completed)
            add_segment(gantt, "IDLE", now, next_arrival)
            now = next_arrival
            continue
        p = min(ready, key=lambda x: (remaining[x.pid], x.arrival, x.pid))
        if p.pid not in first:
            first[p.pid] = now
        add_segment(gantt, p.pid, now, now + 1)
        remaining[p.pid] -= 1
        now += 1
        if remaining[p.pid] == 0:
            completed.add(p.pid)
    return finalize(processes, gantt, first)


def round_robin(processes: List[Process], quantum: int):
    validate_processes(processes)
    if not isinstance(quantum, int) or quantum <= 0:
        raise ValueError("Time quantum must be a positive integer.")
    ordered = sorted(processes, key=lambda x: (x.arrival, x.pid))
    remaining = {p.pid: p.burst for p in processes}
    first, gantt = {}, []
    ready, i, now, completed = deque(), 0, 0, 0

    while completed < len(processes):
        while i < len(ordered) and ordered[i].arrival <= now:
            ready.append(ordered[i])
            i += 1
        if not ready:
            if i < len(ordered):
                add_segment(gantt, "IDLE", now, ordered[i].arrival)
                now = ordered[i].arrival
                continue
            break

        p = ready.popleft()
        if p.pid not in first:
            first[p.pid] = now
        run_for = min(quantum, remaining[p.pid])
        add_segment(gantt, p.pid, now, now + run_for)
        now += run_for
        remaining[p.pid] -= run_for

        # Arrivals during the time slice join before the expired process is re-queued.
        while i < len(ordered) and ordered[i].arrival <= now:
            ready.append(ordered[i])
            i += 1
        if remaining[p.pid] > 0:
            ready.append(p)
        else:
            completed += 1

    return finalize(processes, gantt, first)


def priority_scheduling(processes: List[Process], aging_interval: Optional[int] = None):
    """
    Non-preemptive priority scheduling.
    Lower numeric priority means higher priority.
    Equal effective priorities: earlier arrival, then PID.
    Aging: every aging_interval waiting units improves priority by one,
    bounded at priority 0 (highest).
    """
    validate_processes(processes)
    if aging_interval is not None and aging_interval <= 0:
        raise ValueError("Aging interval must be a positive integer.")
    done, now, gantt, first = set(), 0, [], {}
    while len(done) < len(processes):
        ready = [p for p in processes if p.pid not in done and p.arrival <= now]
        if not ready:
            next_arrival = min(p.arrival for p in processes if p.pid not in done)
            add_segment(gantt, "IDLE", now, next_arrival)
            now = next_arrival
            continue

        def rank(p):
            waited = now - p.arrival
            improvement = (waited // aging_interval) if aging_interval else 0
            effective = max(0, p.priority - improvement)
            return (effective, p.arrival, p.pid)

        p = min(ready, key=rank)
        first[p.pid] = now
        add_segment(gantt, p.pid, now, now + p.burst)
        now += p.burst
        done.add(p.pid)
    return finalize(processes, gantt, first)


def print_result(name, result):
    print(f"\\n=== {name} ===")
    print("Gantt:", " | ".join(
        f'{s["pid"]}[{s["start"]}-{s["end"]}]' for s in result["gantt"]))
    print("PID  AT  BT  CT  TAT  WT  RT")
    for r in result["processes"]:
        print(f'{r["pid"]:<4} {r["arrival"]:>2}  {r["burst"]:>2}  '
              f'{r["completion"]:>2}  {r["turnaround"]:>3}  '
              f'{r["waiting"]:>2}  {r["response"]:>2}')
    a = result["averages"]
    print(f'Average WT={a["waiting"]:.2f}, TAT={a["turnaround"]:.2f}, '
          f'RT={a["response"]:.2f}')
    print(f'Throughput={result["throughput"]:.3f} processes/unit, '
          f'CPU utilization={result["cpu_utilization"]:.1f}%')


def load_csv(path):
    processes = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            processes.append(Process(
                row["pid"], int(row["arrival"]), int(row["burst"]),
                int(row.get("priority", 0))))
    return processes


def main():
    parser = argparse.ArgumentParser(description="CPU Scheduling Simulator")
    parser.add_argument("--input", help="CSV with pid,arrival,burst,priority")
    parser.add_argument("--quantum", type=int, default=2)
    parser.add_argument("--aging", type=int, default=4,
                        help="Priority aging interval; use 0 to disable")
    args = parser.parse_args()

    if args.input:
        processes = load_csv(args.input)
    else:
        processes = [
            Process("P1", 0, 7, 2), Process("P2", 2, 4, 1),
            Process("P3", 4, 1, 3), Process("P4", 5, 4, 2)
        ]

    results = [
        ("FCFS", fcfs(processes)),
        ("SJF", sjf(processes)),
        ("SRTF", srtf(processes)),
        (f"Round Robin (q={args.quantum})", round_robin(processes, args.quantum)),
        ("Priority + Aging", priority_scheduling(
            processes, args.aging if args.aging > 0 else None))
    ]
    for name, result in results:
        print_result(name, result)


if __name__ == "__main__":
    main()
