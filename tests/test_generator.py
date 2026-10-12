import random
import os


# Create a valid S1 test case
def generate_s1(n, rng=None):
    rng = rng or random
    costs = []

    for i in range(n):
        costs.append(rng.randint(1, 99999))

    # S1 costs must go from high to low
    costs.sort(reverse=True)

    return costs


# Create a valid S2 test case
def generate_s2(n, rng=None):
    rng = rng or random

    if n < 3:
        raise ValueError("Problem S2 requires at least three panels")

    # Pick a peak somewhere between the first and last panel
    peak = rng.randint(1, n - 2)

    left = []
    right = []

    # Create the costs before the peak
    for i in range(peak):
        left.append(rng.randint(1, 50000))

    # Create the costs after the peak
    for i in range(n - peak - 1):
        right.append(rng.randint(1, 50000))

    # Costs increase before the peak
    left.sort()

    # Costs decrease after the peak
    right.sort(reverse=True)

    # 99999 is the unique highest cost
    costs = left + [99999] + right

    return costs


# Save a test case to a file
def save_file(filename, n, k, costs):
    file = open(filename, "w")

    file.write(str(n) + " " + str(k) + "\n")

    for i in range(len(costs)):
        file.write(str(costs[i]))

        if i != len(costs) - 1:
            file.write(" ")

    file.write("\n")
    file.close()


def main():
    # A fixed seed makes regenerated correctness files reproducible.
    rng = random.Random(4533)
    os.makedirs("tests/generated", exist_ok=True)

    sizes = [10, 100, 1000, 5000]
    k = 3

    for n in sizes:
        current_k = min(k, n)
        save_file(
            "tests/generated/s1_n" + str(n) + ".txt",
            n,
            current_k,
            generate_s1(n, rng),
        )
        save_file(
            "tests/generated/s2_n" + str(n) + ".txt",
            n,
            current_k,
            generate_s2(n, rng),
        )

    print("Test files were created.")


if __name__ == "__main__":
    main()
