"""Create Plot 9 for Milestone 2."""

import random
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Main project folder
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from program1 import program1
from program5 import program5


OUTPUT_DIR = ROOT / "benchmarks" / "results" / "milestone2"


# Use evenly spaced input sizes
INPUT_SIZES = [
    1000,
    2000,
    3000,
    4000,
    5000,
    6000,
    7000,
    8000,
    9000,
    10000,
]

# Use many random datasets for every input size
TRIALS_PER_SIZE = 50


def get_k(n):
    # Use the same relationship as the other experiments
    return max(1, (n + 9) // 10)


def generate_costs(n):
    costs = []

    for i in range(n):
        costs.append(
            random.randint(1, 99999)
        )

    return costs


def average_relative_excess(n):
    k = get_k(n)

    total_relative_excess = 0

    for trial in range(TRIALS_PER_SIZE):

        costs = generate_costs(n)

        # Eg = energy produced by greedy Program 1
        greedy_energy, greedy_route = program1(
            n,
            k,
            costs,
        )

        # Eo = optimal energy produced by Program 5
        optimal_energy, optimal_route = program5(
            n,
            k,
            costs,
        )

        # Relative excess = (Eg - Eo) / Eo
        relative_excess = (
            greedy_energy - optimal_energy
        ) / optimal_energy

        total_relative_excess += relative_excess

    average = (
        total_relative_excess
        / TRIALS_PER_SIZE
    )

    return average


def main():
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Makes the experiment repeatable
    random.seed(4533)

    average_excesses = []

    for n in INPUT_SIZES:

        average = average_relative_excess(n)

        average_excesses.append(average)

        print(
            "n =",
            n,
            "k =",
            get_k(n),
            "average relative excess =",
            round(average, 4),
        )

    # Create Plot 9
    plt.figure(figsize=(8, 5))

    plt.plot(
        INPUT_SIZES,
        average_excesses,
        marker="o",
    )

    plt.title(
        "Plot 9: Relative Excess Cost of Greedy Algorithm 1"
    )

    plt.xlabel(
        "Input size, n (panels)"
    )

    plt.ylabel(
        "Average relative excess cost"
    )

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "plot9_greedy_quality.png"
    )

    plt.close()

    print()
    print("Plot 9 was created.")


if __name__ == "__main__":
    main()