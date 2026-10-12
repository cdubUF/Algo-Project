from typing import List, Tuple


def program2(n: int, k: int, costs: List[int]) -> Tuple[int, List[int]]:
    """
    Solution to Program 2
    
    Parameters:
    n (int): number of panels
    k (int): maximum number of positions in a forward jump
    costs (List[int]): the landing costs of the panels

    Returns:
    int:  minimum total energy cost
    List[int]: the indices of the visited panels in increasing order(1-indexed, including n and excluding 0)
    """
    
    # S2 has one unique maximum. An optimal route has a jump that crosses
    # (or starts/ends at) that peak; otherwise it would have to move backward.
    peak = max(range(1, n + 1), key=lambda panel: costs[panel - 1])

    # On the increasing side, once an endpoint is fixed, each predecessor
    # should be k positions earlier: moving it any farther right only raises
    # its cost. prefix_cost[i] is the cost of that forced route from 0 to i.
    prefix_cost = [0] * (n + 1)
    for panel in range(1, n + 1):
        prefix_cost[panel] = (
            costs[panel - 1] + prefix_cost[max(0, panel - k)]
        )

    # Symmetrically, costs decrease after the peak, so every jump after a
    # fixed starting panel should go the full k positions (or finish at n).
    suffix_cost = [0] * (n + 1)
    suffix_cost[n] = costs[n - 1]
    for panel in range(n - 1, 0, -1):
        suffix_cost[panel] = (
            costs[panel - 1] + suffix_cost[min(n, panel + k)]
        )

    # Any peak-crossing jump shorter than k can be extended toward a no-more-
    # expensive panel. Therefore it is enough to scan full-length jumps a->a+k
    # that contain the peak. There are at most k of them, so the total is O(n).
    first_start = max(0, peak - k)
    last_start = min(peak, n - k)
    crossing_start = min(
        range(first_start, last_start + 1),
        key=lambda start: prefix_cost[start] + suffix_cost[start + k],
    )
    crossing_end = crossing_start + k

    # Reconstruct the forced prefix in reverse, then append the forced suffix.
    prefix = []
    panel = crossing_start
    while panel > 0:
        prefix.append(panel)
        panel = max(0, panel - k)
    prefix.reverse()

    suffix = []
    panel = crossing_end
    while True:
        suffix.append(panel)
        if panel == n:
            break
        panel = min(n, panel + k)

    route = prefix + suffix
    total_cost = prefix_cost[crossing_start] + suffix_cost[crossing_end]
    return total_cost, route


if __name__ == '__main__':
    n, k = map(int, input().split())
    costs = list(map(int, input().split()))

    m, indices = program2(n, k, costs)

    print(m)
    print(len(indices))
    for i in indices:
        print(i)
