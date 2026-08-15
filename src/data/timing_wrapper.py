import time
from contextlib import contextmanager

class BatchTimer:
    """Tracks per-batch data-load time vs compute time."""

    def __init__(self):
        self.load_times = []
        self.compute_times = []

    @contextmanager
    def track_load(self):
        start = time.perf_counter()
        yield
        self.load_times.append(time.perf_counter() - start)

    @contextmanager
    def track_compute(self):
        start = time.perf_counter()
        yield
        self.compute_times.append(time.perf_counter() - start)

    def summary(self):
        total_load = sum(self.load_times)
        total_compute = sum(self.compute_times)
        total = total_load + total_compute
        return {
            "num_batches": len(self.load_times),
            "total_load_s": round(total_load, 4),
            "total_compute_s": round(total_compute, 4),
            "load_pct": round(100 * total_load / total, 2) if total > 0 else 0,
            "compute_pct": round(100 * total_compute / total, 2) if total > 0 else 0,
        }


if __name__ == "__main__":
    # quick local sanity test with dummy data, no GPU needed
    import random

    timer = BatchTimer()
    for _ in range(5):
        with timer.track_load():
            time.sleep(random.uniform(0.01, 0.05))  # simulate data loading
        with timer.track_compute():
            time.sleep(random.uniform(0.02, 0.08))  # simulate compute

    print(timer.summary())