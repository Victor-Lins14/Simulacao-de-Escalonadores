import pytest
from services.srtf import srtf


def procs(*args):
    return [{"pid": f"P{i+1}", "arrival": a, "burst": b}
            for i, (a, b) in enumerate(args)]


class TestSRTF:
    def test_single_process_no_wait(self):
        gantt, metrics, tme, tmt = srtf(procs((0, 4)))
        assert metrics[0]["ct"] == 4
        assert metrics[0]["wt"] == 0

    def test_gantt_covers_all_burst_time(self):
        p = procs((0, 4), (1, 3), (2, 5))
        gantt, metrics, tme, tmt = srtf(p)
        total_exec = sum(g["end"] - g["start"] for g in gantt)
        assert total_exec == sum(proc["burst"] for proc in p)

    def test_preemption_shorter_job_finishes_first(self):
        # P2 arrives at t=1 with burst=1, should preempt P1 (remaining=3)
        gantt, metrics, tme, tmt = srtf(procs((0, 4), (1, 1)))
        p1 = next(m for m in metrics if m["pid"] == "P1")
        p2 = next(m for m in metrics if m["pid"] == "P2")
        assert p2["ct"] < p1["ct"]
        assert p2["ct"] == 2

    def test_late_arrival_starts_at_arrival_time(self):
        gantt, metrics, tme, tmt = srtf(procs((5, 3)))
        assert gantt[0]["start"] == 5

    def test_turnaround_equals_completion_minus_arrival(self):
        gantt, metrics, tme, tmt = srtf(procs((0, 4), (1, 3), (2, 5)))
        for m in metrics:
            assert m["tat"] == m["ct"] - m["arrival"]

    def test_waiting_equals_turnaround_minus_burst(self):
        gantt, metrics, tme, tmt = srtf(procs((0, 4), (1, 3), (2, 5)))
        for m in metrics:
            assert m["wt"] == m["tat"] - m["burst"]

    def test_average_metrics_match_per_process_values(self):
        gantt, metrics, tme, tmt = srtf(procs((0, 4), (1, 3), (2, 5)))
        assert abs(tme - sum(m["wt"]  for m in metrics) / len(metrics)) < 1e-9
        assert abs(tmt - sum(m["tat"] for m in metrics) / len(metrics)) < 1e-9

    def test_all_processes_complete(self):
        p = procs((0, 4), (1, 3), (2, 5))
        gantt, metrics, tme, tmt = srtf(p)
        assert {m["pid"] for m in metrics} == {proc["pid"] for proc in p}

    def test_no_negative_waiting_time(self):
        gantt, metrics, tme, tmt = srtf(procs((0, 5), (2, 2), (4, 1)))
        assert all(m["wt"] >= 0 for m in metrics)

    def test_known_output_preemptive(self):
        # P1(0,4) P2(1,1) — P2 preempts P1 at t=1, finishes at t=2, P1 at t=5
        gantt, metrics, tme, tmt = srtf(procs((0, 4), (1, 1)))
        ct = {m["pid"]: m["ct"] for m in metrics}
        assert ct["P2"] == 2
        assert ct["P1"] == 5
