from program1 import program1
from program2 import program2


def main():
    choice = input("Choose Program 1 or Program 2: ")

    n, k = map(int, input("Enter n and k: ").split())
    costs = list(map(int, input("Enter panel costs: ").split()))

    if choice == "1":
        total_cost, route = program1(n, k, costs)
    elif choice == "2":
        total_cost, route = program2(n, k, costs)
    else:
        print("Invalid choice.")
        return

    print("Total cost:", total_cost)
    print("Panels visited:", route)


if __name__ == "__main__":
    main()