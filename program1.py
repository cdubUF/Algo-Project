from typing import List, Tuple


def program1(n: int, k: int, costs: List[int]) -> Tuple[int, List[int]]:
    """
    Solution to Program 1
    
    Parameters:
    n (int): number of panels
    k (int): maximum number of positions in a forward jump
    costs (List[int]): the landing costs of the panels

    Returns:
    int:  minimum total energy cost
    List[int]: the indices of the visited panels in increasing order(1-indexed, including n and excluding 0)
    """
    total_cost = 0
    visited_panels = []
    current_position = 0

    # Keep jumping until we reach the last panel
    while current_position < n:

        # Jump as far as possible without going past n
        next_position = min(current_position + k, n)

        # Save the selected panel.
        visited_panels.append(next_position)

        # Add the cost of landing on this panel
        total_cost += costs[next_position - 1]

        # Move to the new panel
        current_position = next_position

    return total_cost, visited_panels


if __name__ == '__main__':

    # Read n and k
    n, k = map(int, input().split())

    # Read the panel costs
    costs = list(map(int, input().split()))

    # Run Program 1
    m, indices = program1(n, k, costs)

    print(m)
    print(len(indices))
    for i in indices:
        print(i)