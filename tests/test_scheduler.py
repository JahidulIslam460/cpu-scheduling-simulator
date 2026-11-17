import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from main import (Process, fcfs, sjf, srtf, round_robin,
                  priority_scheduling, validate_processes)


class SchedulingTests(unittest.TestCase):
    def setUp(self):
        self.jobs = [Process("P1", 0, 5, 2),
                     Process("P2", 1, 3, 1),
                     Process("P3", 2, 2, 1)]

    def test_fcfs_completion_and_waiting(self):
        result = fcfs(self.jobs)
        self.assertEqual([p["completion"] for p in result["processes"]], [5, 8, 10])
        self.assertEqual([p["waiting"] for p in result["processes"]], [0, 4, 6])

    def test_sjf_selects_shortest_ready_job(self):
        result = sjf(self.jobs)
        self.assertEqual([s["pid"] for s in result["gantt"]], ["P1", "P3", "P2"])

    def test_srtf_preempts_when_shorter_job_arrives(self):
        jobs = [Process("P1", 0, 8), Process("P2", 2, 2)]
        result = srtf(jobs)
        self.assertEqual(result["gantt"][0], {"pid": "P1", "start": 0, "end": 2})
        self.assertEqual(result["gantt"][1], {"pid": "P2", "start": 2, "end": 4})

    def test_round_robin_respects_quantum(self):
        result = round_robin(self.jobs, 2)
        self.assertEqual(result["gantt"][0]["end"] - result["gantt"][0]["start"], 2)
        self.assertEqual(len(result["processes"]), 3)

    def test_priority_tie_breaks_by_arrival_then_pid(self):
        jobs = [Process("P2", 0, 1, 1), Process("P1", 0, 2, 1)]
        result = priority_scheduling(jobs)
        self.assertEqual(result["gantt"][0]["pid"], "P1")

    def test_idle_cpu_period(self):
        jobs = [Process("P1", 3, 2), Process("P2", 8, 1)]
        result = fcfs(jobs)
        self.assertEqual(result["gantt"][0], {"pid": "IDLE", "start": 0, "end": 3})

    def test_simultaneous_arrivals_are_all_scheduled(self):
        jobs = [Process("P1", 0, 2), Process("P2", 0, 1), Process("P3", 0, 3)]
        result = fcfs(jobs)
        self.assertEqual([s["pid"] for s in result["gantt"]], ["P1", "P2", "P3"])

    def test_arrivals_during_round_robin_slice_are_queued(self):
        jobs = [Process("P1", 0, 5), Process("P2", 1, 1)]
        result = round_robin(jobs, 3)
        self.assertEqual(result["gantt"][0]["pid"], "P1")
        self.assertEqual(result["gantt"][1]["pid"], "P2")

    def test_metrics_relationship(self):
        result = fcfs(self.jobs)
        for p in result["processes"]:
            self.assertEqual(p["turnaround"], p["completion"] - p["arrival"])
            self.assertEqual(p["waiting"], p["turnaround"] - p["burst"])
            self.assertGreaterEqual(p["response"], 0)

    def test_aging_changes_effective_priority(self):
        # At time 4, L has waited long enough to improve from priority 4 to 2.
        jobs = [Process("H", 0, 4, 0), Process("L", 0, 2, 4),
                Process("M", 4, 1, 2)]
        without_aging = priority_scheduling(jobs, None)
        with_aging = priority_scheduling(jobs, 1)
        start_no_age = next(s["start"] for s in without_aging["gantt"] if s["pid"] == "L")
        start_age = next(s["start"] for s in with_aging["gantt"] if s["pid"] == "L")
        self.assertLess(start_age, start_no_age)

    def test_invalid_quantum(self):
        with self.assertRaises(ValueError):
            round_robin(self.jobs, 0)

    def test_invalid_burst(self):
        with self.assertRaises(ValueError):
            validate_processes([Process("P1", 0, 0)])

    def test_duplicate_pid(self):
        with self.assertRaises(ValueError):
            validate_processes([Process("P1", 0, 1), Process("P1", 2, 1)])

    def test_negative_arrival(self):
        with self.assertRaises(ValueError):
            validate_processes([Process("P1", -1, 2)])


if __name__ == "__main__":
    unittest.main()
