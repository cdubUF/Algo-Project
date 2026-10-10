import random
import os


# Make a folder for the generated test files
os.makedirs("tests/generated", exist_ok=True)


# Create a valid S1 test case
def generate_s1(n):
    costs = []

    for i in range(n):
        costs.append(random.randint(1, 99999))

    # S1 costs must go from high to low
    costs.sort(reverse=True)

    return costs


# Create a valid S2 test case
def generate_s2(n):
    # Pick a peak somewhere between the first and last panel
    peak = random.randint(1, n - 2)

    left = []
    right = []

    # Create the costs before the peak
    for i in range(peak):
        left.append(random.randint(1, 50000))

    # Create the costs after the peak
    for i in range(n - peak - 1):
        right.append(random.randint(1, 50000))

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


# Different input sizes to test
sizes = [10, 100, 1000, 5000]

k = 3


for n in sizes:
    current_k = min(k, n)

    s1_costs = generate_s1(n)
    s2_costs = generate_s2(n)

    save_file(
        "tests/generated/s1_n" + str(n) + ".txt",
        n,
        current_k,
        s1_costs
    )

    save_file(
        "tests/generated/s2_n" + str(n) + ".txt",
        n,
        current_k,
        s2_costs
    )


print("Test files were created.")