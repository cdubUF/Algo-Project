import random
import os


# Folder where the generated test files will go
os.makedirs("tests/generated/milestone2", exist_ok=True)


# Use the same random numbers each time
random.seed(4533)


def generate_general(n):
    costs = []

    for i in range(n):
        costs.append(random.randint(1, 99999))

    return costs


def save_file(filename, n, k, costs):
    file = open(filename, "w")

    file.write(str(n) + " " + str(k) + "\n")

    for i in range(len(costs)):
        file.write(str(costs[i]))

        if i != len(costs) - 1:
            file.write(" ")

    file.write("\n")
    file.close()


# These sizes are used for the different programs
sizes = [
    21,
    22,
    23,
    24,
    25,
    100,
    250,
    500,
    1000,
    2000,
    3000,
    5000,
    10000,
    25000,
    50000,
    75000,
    99000,
]


for n in sizes:

    # k = ceil(n / 10)
    k = max(1, (n + 9) // 10)

    costs = generate_general(n)

    filename = (
        "tests/generated/milestone2/general_n"
        + str(n)
        + ".txt"
    )

    save_file(
        filename,
        n,
        k,
        costs,
    )


print("Milestone 2 test files were created.")