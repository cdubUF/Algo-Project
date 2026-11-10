"""Create Plots 3-8 for Milestone 2."""

import sys
from pathlib import Path
from time import perf_counter

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Main project folder
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from program3 import program3
from program4A import program4A
from program4B import program4B
from program5 import program5


TEST_DIR = ROOT / "tests" / "generated" / "milestone2"
OUTPUT_DIR = ROOT / "benchmarks" / "results" / "milestone2"


# Program 3 is exponential
PROGRAM3_SIZES = [21, 22, 23, 24, 25]

# Programs 4A and 4B are Theta(nk)
PROGRAM4_SIZES = [
    100,
    250,
    500,
    1000,
    2000,
    3000,
    5000,
]

# Program 5 is Theta(n)
PROGRAM5_SIZES = [
    1000,
    5000,
    10000,
    25000,
    50000,
    75000,
    99000,
]


def load_file(n):
    filename = TEST_DIR / ("general_n" + str(n) + ".txt")

    file = open(filename, "r")

    first_line = file.readline().split()
    second_line = file.readline().split()

    file.close()

    file_n = int(first_line[0])
    k = int(first_line[1])

    costs = []

    for value in second_line:
        costs.append(int(value))

    return file_n, k, costs


def measure_time(program, n):
    file_n, k, costs = load_file(n)

    # Start timer
    start = perf_counter()

    # Run program
    program(file_n, k, costs)

    # Stop timer
    end = perf_counter()

    # Convert seconds to milliseconds
    runtime = (end - start) * 1000

    return runtime, k


def benchmark(program, sizes):
    runtimes = []

    for n in sizes:

        runtime, k = measure_time(program, n)

        runtimes.append(runtime)

        print(
            "n =",
            n,
            "k =",
            k,
            "runtime =",
            round(runtime, 4),
            "ms",
        )

    return runtimes


def make_plot(sizes, runtimes, title, filename):
    plt.figure(figsize=(8, 5))

    plt.plot(
        sizes,
        runtimes,
        marker="o",
    )

    plt.title(title)

    plt.xlabel("Input size, n (panels)")
    plt.ylabel("Running time (milliseconds)")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / filename
    )

    plt.close()

def make_plot7(
    program3_times,
    program4A_times,
    program4B_times,
    program5_times,
):

    """Compare Programs 3, 4A, 4B, and 5."""

    plt.figure(figsize=(8, 5))

    plt.plot(
        PROGRAM3_SIZES,
        program3_times,
        marker="o",
        label="Program 3",
    )

    plt.plot(
        PROGRAM4_SIZES,
        program4A_times,
        marker="o",
        label="Program 4A",
    )

    plt.plot(
        PROGRAM4_SIZES,
        program4B_times,
        marker="o",
        label="Program 4B",
    )

    plt.plot(
        PROGRAM5_SIZES,
        program5_times,
        marker="o",
        label="Program 5",
    )

    # Log scales make all four programs visible even though
    # their input sizes and running times are very different.
    plt.xscale("log")
    plt.yscale("log")

    plt.title(
        "Plot 7: Running Time Comparison of Programs 3, 4A, 4B, and 5"
    )

    plt.xlabel("Input size, n (panels) - log scale")
    plt.ylabel("Running time (milliseconds) - log scale")

    plt.grid(True)
    plt.legend()

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "plot7_all_programs.png"
    )

    plt.close()


def make_plot8(program4A_times, program4B_times):
    """Compare Program 4A and Program 4B."""

    plt.figure(figsize=(8, 5))

    plt.plot(
        PROGRAM4_SIZES,
        program4A_times,
        marker="o",
        label="Program 4A",
    )

    plt.plot(
        PROGRAM4_SIZES,
        program4B_times,
        marker="o",
        label="Program 4B",
    )

    plt.title(
        "Plot 8: Program 4A vs. Program 4B Running Time"
    )

    plt.xlabel("Input size, n (panels)")
    plt.ylabel("Running time (milliseconds)")

    plt.grid(True)
    plt.legend()

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "plot8_program4A_vs_program4B.png"
    )

    plt.close()


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Program 3")
    program3_times = benchmark(
        program3,
        PROGRAM3_SIZES,
    )

    print()
    print("Program 4A")
    program4A_times = benchmark(
        program4A,
        PROGRAM4_SIZES,
    )

    print()
    print("Program 4B")
    program4B_times = benchmark(
        program4B,
        PROGRAM4_SIZES,
    )

    print()
    print("Program 5")
    program5_times = benchmark(
        program5,
        PROGRAM5_SIZES,
    )

    make_plot(
        PROGRAM3_SIZES,
        program3_times,
        "Plot 3: Program 3 Running Time vs. Input Size",
        "plot3_program3.png",
    )

    make_plot(
        PROGRAM4_SIZES,
        program4A_times,
        "Plot 4: Program 4A Running Time vs. Input Size",
        "plot4_program4A.png",
    )

    make_plot(
        PROGRAM4_SIZES,
        program4B_times,
        "Plot 5: Program 4B Running Time vs. Input Size",
        "plot5_program4B.png",
    )

    make_plot(
        PROGRAM5_SIZES,
        program5_times,
        "Plot 6: Program 5 Running Time vs. Input Size",
        "plot6_program5.png",
    )

    # Plot 7
    make_plot7(
        program3_times,
        program4A_times,
        program4B_times,
        program5_times,
    )

    # Plot 8
    make_plot8(
        program4A_times,
        program4B_times,
    )

    print()
    print("Plots 3-8 were created.")


if __name__ == "__main__":
    main()