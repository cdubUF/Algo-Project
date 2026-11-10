from typing import List, Tuple


def program3(n: int, k: int, costs: List[int]) -> Tuple[int, List[int]]:
    """
    Solution to Program 3
    
    Parameters:
    n (int): number of panels
    k (int): maximum number of positions in a forward jump
    costs (List[int]): the landing costs of the panels

    Returns:
    int:  minimum total energy cost
    List[int]: the indices of the visited panels in increasing order(1-indexed, including n and excluding 0)
    """
    # Find the cheapest route starting from a given position
    def solve(position):
        # If we reached panel n, there is no more cost
        if position == n:
            return 0, []

        best_cost = float("inf")
        best_route = []

        # Try every possible next jump
        last_panel = min(position + k, n)

        for next_panel in range(position + 1, last_panel + 1):

            # Find the best route after landing on next_panel
            remaining_cost, remaining_route = solve(next_panel)

            # Add the cost of landing on this panel
            total_cost = costs[next_panel - 1] + remaining_cost

            # Save this route if it is cheaper
            if total_cost < best_cost:
                best_cost = total_cost
                best_route = [next_panel] + remaining_route

        return best_cost, best_route

    # Start from position 0
    return solve(0)


if __name__ == '__main__':
    n, k = map(int, input().split())
    costs = list(map(int, input().split()))

    m, indices = program3(n, k, costs)

    print(m)
    print(len(indices))
    for i in indices:
        print(i)