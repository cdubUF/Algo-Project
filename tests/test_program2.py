import itertools
import subprocess
import sys
import unittest
from pathlib import Path

from program2 import program2


ROOT = Path(__file__).resolve().parents[1]


def exhaustive_solution(n, k, costs):
    """Independent small-input oracle for the unrestricted routing problem."""
    best = [None] * (n + 1)
    best[0] = (0, [])

    for panel in range(1, n + 1):
        candidates = []
        for previous in range(max(0, panel - k), panel):
            if best[previous] is not None:
                energy, route = best[previous]
                candidates.append((energy + costs[panel - 1], route + [panel]))
        best[panel] = min(candidates)

    return best[n]


def reference_minimum_cost(n, k, costs):
    """Straightforward O(nk) DP oracle suitable for the generated files."""
    minimum = [0] + [float("inf")] * n
    for panel in range(1, n + 1):
        minimum[panel] = costs[panel - 1] + min(
            minimum[max(0, panel - k):panel]
        )
    return minimum[n]


def assert_valid_route(test_case, n, k, costs, result):
    energy, route = result
    test_case.assertTrue(route)
    test_case.assertEqual(route[-1], n)
    test_case.assertEqual(route, sorted(route))
    test_case.assertEqual(len(route), len(set(route)))
    test_case.assertTrue(all(1 <= panel <= n for panel in route))

    positions = [0] + route
    test_case.assertTrue(
        all(1 <= current - previous <= k
            for previous, current in zip(positions, positions[1:]))
    )
    test_case.assertEqual(energy, sum(costs[panel - 1] for panel in route))


class Program2Tests(unittest.TestCase):
    def assert_optimal(self, n, k, costs):
        actual = program2(n, k, costs)
        assert_valid_route(self, n, k, costs, actual)
        self.assertEqual(actual[0], exhaustive_solution(n, k, costs)[0])

    def test_assignment_example_3(self):
        self.assertEqual(
            program2(10, 4, [1, 2, 4, 9, 12, 10, 6, 4, 3, 1]),
            (11, [3, 7, 10]),
        )

    def test_peak_must_be_avoided_with_an_extra_landing(self):
        self.assertEqual(program2(4, 2, [1, 100, 2, 1]), (4, [1, 3, 4]))

    def test_k_one_visits_every_panel_including_peak(self):
        self.assertEqual(program2(5, 1, [1, 3, 9, 4, 2]), (19, [1, 2, 3, 4, 5]))

    def test_k_equal_to_n_jumps_directly_to_final_panel(self):
        self.assertEqual(program2(5, 5, [1, 3, 9, 4, 2]), (2, [5]))

    def test_small_valid_s2_inputs_match_exhaustive_oracle(self):
        # Exhaustively vary each strictly increasing/decreasing step. This checks
        # the greedy design itself rather than a few hard-coded expected routes.
        for n in range(3, 9):
            for peak in range(1, n - 1):
                for deltas in itertools.product((1, 2), repeat=n - 1):
                    left = [1]
                    for delta in deltas[:peak]:
                        left.append(left[-1] + delta)

                    right = []
                    value = left[-1]
                    for delta in deltas[peak:]:
                        value -= delta
                        right.append(value)

                    if right and min(right) < 1:
                        continue
                    costs = left + right
                    for k in range(1, n + 1):
                        with self.subTest(n=n, k=k, peak=peak, costs=costs):
                            self.assert_optimal(n, k, costs)

    def test_generated_s2_datasets(self):
        for path in sorted((ROOT / "tests" / "generated").glob("s2_n*.txt")):
            values = [int(value) for value in path.read_text().split()]
            n, k = values[:2]
            costs = values[2:]
            with self.subTest(path=path.name):
                self.assertEqual(len(costs), n)
                result = program2(n, k, costs)
                assert_valid_route(self, n, k, costs, result)
                self.assertEqual(result[0], reference_minimum_cost(n, k, costs))

    def test_cli_output_contract(self):
        completed = subprocess.run(
            [sys.executable, str(ROOT / "program2.py")],
            input="10 4\n1 2 4 9 12 10 6 4 3 1\n",
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertEqual(completed.stdout.splitlines(), ["11", "3", "3", "7", "10"])


if __name__ == "__main__":
    unittest.main()
