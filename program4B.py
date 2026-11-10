from typing import List, Tuple


def program4B(n: int, k: int, costs: List[int]) -> Tuple[int, List[int]]:
    """Solve the general panel problem with bottom-up O(nk) DP."""
    minimum = [0] + [0] * n
    predecessor = [-1] * (n + 1)

    # All dependencies of panel i have already been evaluated because they
    # have smaller indices.  Ties choose the earlier predecessor.
    for panel in range(1, n + 1):
        best_previous = min(
            range(max(0, panel - k), panel),
            key=lambda previous: (minimum[previous], previous),
        )
        minimum[panel] = minimum[best_previous] + costs[panel - 1]
        predecessor[panel] = best_previous

    # Recover the selected path from the predecessor links.
    route = []
    panel = n
    while panel:
        route.append(panel)
        panel = predecessor[panel]
    route.reverse()
    return minimum[n], route


if __name__ == "__main__":
    n, k = map(int, input().split())
    costs = list(map(int, input().split()))

    minimum_energy, indices = program4B(n, k, costs)
    print(minimum_energy)
    print(len(indices))
    for index in indices:
        print(index)
