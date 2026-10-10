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

    # Greedily jump as far forward as possible at each step.
    # If fewer than k positions remain, jump directly to panel n.
    while current_position < n:
        next_position = min(current_position + k, n)

        # Save the selected panel.
        visited_panels.append(next_position)

        # Panel numbers are 1-indexed, while the costs list is 0-indexed.
        total_cost += costs[next_position - 1]

        current_position = next_position

    return total_cost, visited_panels

    return 0, [1, 2, 3] # replace with your code


if __name__ == '__main__':
    n, k = map(int, input().split())
    costs = list(map(int, input().split()))

    m, indices = program1(n, k, costs)

    print(m)
    print(len(indices))
    for i in indices:
        print(i)