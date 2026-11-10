import random
import subprocess
import sys
import unittest
from pathlib import Path

from program3 import program3
from program4A import program4A
from program4B import program4B
from program5 import program5


ROOT = Path(__file__).resolve().parents[1]
PROGRAMS = (program3, program4A, program4B, program5)
SEEDS = (4533, 20261109)


def reference_solution(n, k, costs):
    minimum = [0] + [float("inf")] * n
    predecessor = [-1] * (n + 1)
    for panel in range(1, n + 1):
        previous = min(
            range(max(0, panel - k), panel),
            key=lambda index: (minimum[index], index),
        )
        minimum[panel] = minimum[previous] + costs[panel - 1]
        predecessor[panel] = previous

    route = []
    panel = n
    while panel:
        route.append(panel)
        panel = predecessor[panel]
    return minimum[n], list(reversed(route))


def assert_valid_route(test_case, n, k, costs, result):
    energy, route = result
    test_case.assertTrue(route)
    test_case.assertEqual(route[-1], n)
    test_case.assertNotIn(0, route)
    test_case.assertTrue(all(a < b for a, b in zip(route, route[1:])))
    test_case.assertTrue(all(1 <= panel <= n for panel in route))
    positions = [0] + route
    test_case.assertTrue(
        all(1 <= current - previous <= k
            for previous, current in zip(positions, positions[1:]))
    )
    test_case.assertEqual(energy, sum(costs[panel - 1] for panel in route))


class GeneralProgramTests(unittest.TestCase):
    def check_case(self, n, k, costs, include_program3=True):
        expected_energy = reference_solution(n, k, costs)[0]
        selected = PROGRAMS if include_program3 else PROGRAMS[1:]
        for program in selected:
            with self.subTest(program=program.__name__, n=n, k=k, costs=costs):
                result = program(n, k, costs)
                assert_valid_route(self, n, k, costs, result)
                self.assertEqual(result[0], expected_energy)

    def test_assignment_examples_and_boundaries(self):
        cases = (
            (10, 4, [1, 2, 4, 9, 12, 10, 6, 4, 3, 1]),
            (1, 1, [17]),
            (6, 1, [6, 5, 4, 3, 2, 1]),
            (6, 6, [6, 5, 4, 3, 2, 1]),
            (7, 3, [5] * 7),
            (7, 3, list(range(1, 8))),
            (7, 3, list(range(7, 0, -1))),
            (8, 3, [9, 1, 8, 2, 7, 3, 6, 4]),
        )
        for case in cases:
            self.check_case(*case)

    def test_additional_cases(self):
        cases = (
            (2, 1, [4, 9]),
            (2, 2, [99, 1]),
            (3, 2, [8, 1, 7]),
            (3, 3, [1, 100, 5]),
            (4, 2, [3, 3, 3, 3]),
            (4, 3, [10, 1, 1, 10]),
            (5, 2, [9, 8, 7, 6, 5]),
            (5, 3, [1, 2, 3, 4, 5]),
            (6, 2, [1, 99, 1, 99, 1, 99]),
            (6, 4, [99, 1, 99, 1, 99, 1]),
            (7, 2, [4, 8, 15, 16, 23, 42, 7]),
            (7, 4, [12, 5, 9, 2, 11, 3, 8]),
            (8, 2, [20, 1, 18, 2, 16, 3, 14, 4]),
            (8, 5, [2, 50, 50, 50, 1, 50, 50, 2]),
            (9, 3, [7, 1, 9, 2, 8, 3, 6, 4, 5]),
            (9, 8, [100, 90, 80, 70, 60, 50, 40, 30, 20]),
            (10, 2, [5, 5, 1, 5, 5, 1, 5, 5, 1, 5]),
            (10, 6, [13, 21, 8, 34, 5, 55, 3, 89, 2, 1]),
            (12, 4, [6, 2, 9, 1, 8, 3, 7, 4, 10, 5, 11, 2]),
            (15, 7, [31, 4, 28, 7, 25, 10, 22, 13, 19, 16, 1, 18, 6, 24, 3]),
        )
        self.assertEqual(len(cases), 20)
        for case in cases:
            self.check_case(*case)

    def test_independently_verified_answers(self):
        self.assertEqual(reference_solution(4, 2, [1, 100, 2, 1])[0], 4)
        self.assertEqual(reference_solution(5, 5, [8, 7, 6, 5, 4])[0], 4)
        self.assertEqual(reference_solution(5, 1, [1, 2, 3, 4, 5])[0], 15)

    def test_seeded_random_small_inputs(self):
        for seed in SEEDS:
            rng = random.Random(seed)
            for n in range(1, 10):
                for _ in range(8):
                    k = rng.randint(1, n)
                    costs = [rng.randint(1, 99999) for _ in range(n)]
                    self.check_case(n, k, costs)

    def test_repeated_top_down_calls_do_not_share_state(self):
        first = program4A(4, 2, [1, 100, 2, 1])
        second = program4A(4, 2, [100, 1, 100, 1])
        self.assertEqual(first[0], 4)
        self.assertEqual(second[0], 2)

    def test_larger_inputs_without_exponential_program(self):
        rng = random.Random(SEEDS[0])
        for n in (100, 1000):
            k = max(1, n // 10)
            costs = [rng.randint(1, 99999) for _ in range(n)]
            self.check_case(n, k, costs, include_program3=False)

    def test_each_script_uses_the_required_io_contract(self):
        input_text = "4 2\n1 100 2 1\n"
        for name in ("program3.py", "program4A.py", "program4B.py", "program5.py"):
            completed = subprocess.run(
                [sys.executable, str(ROOT / name)],
                input=input_text,
                text=True,
                capture_output=True,
                check=True,
            )
            lines = completed.stdout.splitlines()
            energy = int(lines[0])
            count = int(lines[1])
            route = [int(value) for value in lines[2:]]
            self.assertEqual(count, len(route))
            assert_valid_route(self, 4, 2, [1, 100, 2, 1], (energy, route))
            self.assertEqual(energy, 4)


if __name__ == "__main__":
    unittest.main()
