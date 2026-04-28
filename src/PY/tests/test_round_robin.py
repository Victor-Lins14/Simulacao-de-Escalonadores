import pytest
from services.round_robin import round_robin


def procs(*args):
    return [{"pid": f"P{i+1}", "arrival": a, "burst": b}
            for i, (a, b) in enumerate(args)]


class TestRoundRobin:
    def test_single_process_no_wait(self):
        gantt, metrics, tme, tmt = round_robin(procs((0, 4)), 2)
        assert metrics[0]["ct"] == 4
        assert metrics[0]["wt"] == 0
        assert tme == 0.0

    def test_gantt_covers_all_burst_time(self):
        p = procs((0, 4), (1, 3), (2, 5))
        gantt, metrics, tme, tmt = round_robin(p, 2)
        total_exec = sum(g["end"] - g["start"] for g in gantt)
        assert total_exec == sum(proc["burst"] for proc in p)

    def test_quantum_larger_than_burst_produces_single_block(self):
        gantt, metrics, tme, tmt = round_robin(procs((0, 2)), 10)
        assert len(gantt) == 1
        assert gantt[0]["end"] == 2

    def test_late_arrival_starts_at_arrival_time(self):
        gantt, metrics, tme, tmt = round_robin(procs((5, 3)), 2)
        assert gantt[0]["start"] == 5

    def test_turnaround_equals_completion_minus_arrival(self):
        gantt, metrics, tme, tmt = round_robin(procs((0, 4), (1, 3), (2, 5)), 2)
        for m in metrics:
            assert m["tat"] == m["ct"] - m["arrival"]

    def test_waiting_equals_turnaround_minus_burst(self):
        gantt, metrics, tme, tmt = round_robin(procs((0, 4), (1, 3), (2, 5)), 2)
        for m in metrics:
            assert m["wt"] == m["tat"] - m["burst"]

    def test_average_metrics_match_per_process_values(self):
        gantt, metrics, tme, tmt = round_robin(procs((0, 4), (1, 3), (2, 5)), 2)
        assert abs(tme - sum(m["wt"]  for m in metrics) / len(metrics)) < 1e-9
        assert abs(tmt - sum(m["tat"] for m in metrics) / len(metrics)) < 1e-9

    def test_all_processes_complete(self):
        p = procs((0, 4), (1, 3), (2, 5))
        gantt, metrics, tme, tmt = round_robin(p, 2)
        completed_pids = {m["pid"] for m in metrics}
        assert completed_pids == {proc["pid"] for proc in p}

    def test_processes_with_same_arrival(self):
        gantt, metrics, tme, tmt = round_robin(procs((0, 3), (0, 3)), 2)
        assert len(metrics) == 2
        assert all(m["wt"] >= 0 for m in metrics)

    def test_known_output_quantum_2(self):
        # P1(0,4) P2(1,3) P3(2,5) q=2 — completion times verified manually
        gantt, metrics, tme, tmt = round_robin(procs((0, 4), (1, 3), (2, 5)), 2)
        ct = {m["pid"]: m["ct"] for m in metrics}
        assert ct["P1"] == 8
        assert ct["P2"] == 9
        assert ct["P3"] == 12
