from functools import lru_cache
from typing import List, Tuple


def program4A(n: int, k: int, costs: List[int]) -> Tuple[int, List[int]]:
    """Solve the general panel problem with top-down memoized DP.

    ``minimum(i)`` is the minimum energy needed to land on panel ``i``.
    The predecessor table records the choice used to recover the route.
    """
    
    predecessor = [-1] * (n + 1)

    @lru_cache(maxsize=None)
    def minimum(panel: int) -> int:
        if panel == 0:
            return 0

        best_previous = min(
            range(max(0, panel - k), panel),
            key=lambda previous: (minimum(previous), previous),
        )
        predecessor[panel] = best_previous
        return minimum(best_previous) + costs[panel - 1]

    # Calculate values in smaller groups to avoid deep recursion
    for checkpoint in range(100, n, 100):
        minimum(checkpoint)

    energy = minimum(n)

    # Follow the recorded choices from n to 0, then reverse them so the
    # returned panel indices are strictly increasing.
    route = []
    panel = n
    while panel:
        route.append(panel)
        panel = predecessor[panel]
    route.reverse()
    return energy, route


if __name__ == "__main__":
    n, k = map(int, input().split())
    costs = list(map(int, input().split()))

    minimum_energy, indices = program4A(n, k, costs)
    print(minimum_energy)
    print(len(indices))
    for index in indices:
        print(index)
