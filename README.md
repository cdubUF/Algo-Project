# Algo Project

This repository contains the specialized greedy solutions and four general-case
solutions for the panel-jumping problem, together with reproducible correctness
checks and performance scripts.

## Requirements

- Python 3.10 or newer
- `matplotlib` (needed only for the benchmark plots)

No external package is required to run the algorithms or the unit tests. To
install the plotting dependency, run this from the repository root:

```bash
python -m pip install matplotlib
```

On Windows, use `py` instead of `python` if that is the name of your Python
launcher.

## Run the programs

Each program reads two lines from standard input:

1. `n k`, where `n` is the number of panels and `k` is the maximum jump length.
2. Exactly `n` space-separated panel costs.

For example, run Program 1 with:

```bash
python program1.py
```

Or run Program 2 with the assignment example:

```bash
python program2.py
```

Then enter:

```text
10 4
1 2 4 9 12 10 6 4 3 1
```

The output is the total cost, the number of visited panels, and then one
visited panel index per line. For the Program 2 example above, the expected
output is:

```text
11
3
3
7
10
```

Programs 3, 4A, 4B, and 5 use the same input and output contract. Program 3 is
an exhaustive recursive reference for small inputs. Program 4A is top-down
memoized dynamic programming, Program 4B is bottom-up dynamic programming, and
Program 5 uses a monotonic deque for Theta(n) time. Program 4A raises Python's
recursion limit when necessary because a valid dependency chain can contain all
`n` panels.

`main.py` is also available as an interactive menu for Programs 1 and 2:

```bash
python main.py
```

## Run the correctness tests

From the repository root, run:

```bash
python -m unittest discover -s tests -v
```

The suite checks Programs 3, 4A, 4B, and 5 against an independent dynamic
programming oracle on assignment examples, boundary cases, structured cost
patterns, and randomized small inputs. The random seeds are `4533` and
`20261109`. It validates the first jump from position 0, every later jump,
strictly increasing route indices, final arrival at `n`, and agreement between
reported energy and visited-panel costs. Program 3 is used only on small inputs.
Every general-case script is also exercised through standard input/output.

The committed inputs in `tests/generated/` are sufficient to run the tests. To
recreate those deterministic S1 and S2 files before testing, run:

```bash
python tests/test_generator.py
```

## Reproduce the performance results

Run both benchmark scripts from the repository root:

```bash
python benchmarks/benchmark_program1.py
python benchmarks/benchmark_program2.py
```

Each size receives 3 warm-up runs followed by 15 measured runs. Input creation,
correctness checks, CSV writing, and plotting are outside the timed region. The
scripts plot the median runtime, with the measured minimum and maximum shown as
error bars. Randomly generated benchmark inputs use fixed, size-specific seeds,
so the input data is reproducible; exact timings will vary by computer and by
system load.

The commands overwrite or create these artifacts:

- `benchmarks/results/program1_benchmark.csv`
- `benchmarks/results/plot1_program1.png`
- `benchmarks/results/program2_benchmark.csv`
- `benchmarks/results/plot2_program2.png`
- `benchmarks/results/program2_performance.md`

For a quicker smoke test, reduce the number of measured and warm-up runs and
write the outputs to a separate directory:

```bash
python benchmarks/benchmark_program1.py --repeats 2 --warmups 1 --output-dir benchmarks/smoke-results
python benchmarks/benchmark_program2.py --repeats 2 --warmups 1 --output-dir benchmarks/smoke-results
```

## Performance study

### Plot 1: Program 1

Program 1 was measured from 1,000 through 99,000 panels with `k = 3`. The
submitted median runtime increased from 0.0648 ms at `n = 1,000` to 6.4261 ms
at `n = 99,000`. The linear fit had an R² of approximately 0.9991, consistent
with the expected Θ(n/k) behavior when `k` is constant.

![Program 1 running time](benchmarks/results/plot1_program1.png)

### Plot 2: Program 2

Program 2 used the same input sizes with `k = ceil(n / 10)`, as suggested by
the project instructions. Its measured runtime also increased approximately
linearly with input size, consistent with its Θ(n) implementation.

![Program 2 running time](benchmarks/results/plot2_program2.png)
