from collections import deque
from typing import List, Tuple


def program5(n: int, k: int, costs: List[int]) -> Tuple[int, List[int]]:
    """Solve the general panel problem in Theta(n) time.

    The deque stores candidate predecessor panels in increasing DP-cost order.
    Each panel enters and leaves it at most once, so both optimization and
    route recovery take linear time.
    """
    minimum = [0] * (n + 1)
    predecessor = [-1] * (n + 1)
    candidates = deque([0])

    for panel in range(1, n + 1):
        # Remove panels that are too far behind to reach the current panel.
        while candidates[0] < panel - k:
            candidates.popleft()

        best_previous = candidates[0]
        minimum[panel] = minimum[best_previous] + costs[panel - 1]
        predecessor[panel] = best_previous

        # A more expensive candidate can never be useful after this panel.
        # Keep equal-cost earlier panels to make tie-breaking deterministic.
        while candidates and minimum[candidates[-1]] > minimum[panel]:
            candidates.pop()
        candidates.append(panel)

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

    minimum_energy, indices = program5(n, k, costs)
    print(minimum_energy)
    print(len(indices))
    for index in indices:
        print(index)
