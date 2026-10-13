"""Performance study for Program 1 (Problem S1)."""

import argparse
import csv
import gc
import random
import statistics
import sys
from pathlib import Path
from time import perf_counter_ns

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from program1 import program1


DEFAULT_SIZES = (1_000, 5_000, 10_000, 25_000, 50_000, 75_000, 99_000)

# Keep k constant so the growth of n/k can be observed as n increases.
K = 3


def generate_s1(n):
    """Generate a valid S1 dataset with decreasing costs."""
    rng = random.Random(4533 + n)

    costs = []

    for i in range(n):
        costs.append(rng.randint(1, 99999))

    costs.sort(reverse=True)

    return costs


def load_or_generate_s1(n):
    generated_file = ROOT / "tests" / "generated" / f"s1_n{n}.txt"

    if generated_file.exists():
        values = [int(value) for value in generated_file.read_text().split()]

        file_n = values[0]
        file_k = values[1]
        costs = values[2:]

        if file_n != n or len(costs) != n:
            raise ValueError(f"Invalid generated dataset: {generated_file}")

        if file_k == K:
            return costs, str(generated_file.relative_to(ROOT))

    # Generate the larger datasets without saving huge text files.
    costs = generate_s1(n)

    return costs, "generated in benchmark"


def benchmark_case(n, repeats, warmups):
    costs, dataset_source = load_or_generate_s1(n)
    k = K

    # Warmup runs are not included in the timing results.
    for _ in range(warmups):
        program1(n, k, costs)

    samples_ms = []

    gc.disable()

    try:
        for _ in range(repeats):
            start = perf_counter_ns()

            result = program1(n, k, costs)

            elapsed_ns = perf_counter_ns() - start
            samples_ms.append(elapsed_ns / 1_000_000)

            # Simple correctness check outside the timed section.
            energy, route = result

            assert route[-1] == n
            assert energy == sum(costs[panel - 1] for panel in route)

    finally:
        gc.enable()

    return {
        "n": n,
        "k": k,
        "dataset_source": dataset_source,
        "repetitions": repeats,
        "median_ms": statistics.median(samples_ms),
        "mean_ms": statistics.fmean(samples_ms),
        "min_ms": min(samples_ms),
        "max_ms": max(samples_ms),
    }


def linear_fit(rows):
    xs = [row["n"] for row in rows]
    ys = [row["median_ms"] for row in rows]

    x_mean = statistics.fmean(xs)
    y_mean = statistics.fmean(ys)

    denominator = sum((x - x_mean) ** 2 for x in xs)

    slope = sum(
        (x - x_mean) * (y - y_mean)
        for x, y in zip(xs, ys)
    ) / denominator

    intercept = y_mean - slope * x_mean

    predictions = [
        slope * x + intercept
        for x in xs
    ]

    residual = sum(
        (y - predicted) ** 2
        for y, predicted in zip(ys, predictions)
    )

    total = sum(
        (y - y_mean) ** 2
        for y in ys
    )

    r_squared = 1.0 - residual / total if total else 1.0

    return slope, intercept, r_squared, predictions


def write_csv(rows, path):
    fields = (
        "n",
        "k",
        "dataset_source",
        "repetitions",
        "median_ms",
        "mean_ms",
        "min_ms",
        "max_ms",
    )

    with path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=fields)

        writer.writeheader()
        writer.writerows(rows)


def write_plot(rows, predictions, path):
    sizes = [row["n"] for row in rows]
    medians = [row["median_ms"] for row in rows]

    lower = [
        row["median_ms"] - row["min_ms"]
        for row in rows
    ]

    upper = [
        row["max_ms"] - row["median_ms"]
        for row in rows
    ]

    fig, axis = plt.subplots(figsize=(8, 5), dpi=180)

    axis.errorbar(
        sizes,
        medians,
        yerr=[lower, upper],
        marker="o",
        linewidth=1.8,
        capsize=4,
        label="Median (min-max error bars)",
    )

    axis.plot(
        sizes,
        predictions,
        "--",
        linewidth=1.5,
        label="Linear fit",
    )

    axis.set_title("Plot 1: Program 1 Running Time vs. Input Size")
    axis.set_xlabel("Input size, n (panels)")
    axis.set_ylabel("Execution time (milliseconds)")

    axis.grid(True, alpha=0.3)
    axis.legend()

    fig.tight_layout()
    fig.savefig(path)

    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("--repeats", type=int, default=15)
    parser.add_argument("--warmups", type=int, default=3)

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "benchmarks" / "results",
    )

    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    rows = [
        benchmark_case(n, args.repeats, args.warmups)
        for n in DEFAULT_SIZES
    ]

    slope, intercept, r_squared, predictions = linear_fit(rows)

    write_csv(
        rows,
        args.output_dir / "program1_benchmark.csv",
    )

    write_plot(
        rows,
        predictions,
        args.output_dir / "plot1_program1.png",
    )

    for row in rows:
        print(
            f"n={row['n']:>6}, "
            f"k={row['k']:>2}: "
            f"median={row['median_ms']:.4f} ms"
        )

    print(f"Linear fit R^2={r_squared:.4f}")


if __name__ == "__main__":
    main()