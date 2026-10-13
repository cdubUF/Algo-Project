# Algo-Project

## Performance Study

Both greedy programs were benchmarked using Problem S1 and Problem S2 datasets
with varying input sizes. Multiple runs were performed for each size to reduce
timing inconsistencies. Median execution time was used for the plots, while the
minimum and maximum times were included as error bars.

### Plot 1: Program 1 Running Time

Program 1 was tested with input sizes ranging from 1,000 to 99,000 panels.
The maximum jump length was held constant at k = 3. Each input size received
3 warm-up runs followed by 15 measured runs.

The median runtime increased from 0.0648 ms at n = 1,000 to 6.4261 ms at
n = 99,000. The results followed a nearly linear trend, with an R² value of
approximately 0.9991. This is consistent with the expected Θ(n/k) behavior
when k is kept constant.

[Plot 1](benchmarks/results/plot1_program1.png)

### Plot 2: Program 2 Running Time

Program 2 was tested using the same range of input sizes. For Program 2,
k was set to ceil(n / 10), following the suggestion in the project
instructions.

The measured runtime also increased as input size increased and showed a
strong linear trend.

[Plot 2](benchmarks/results/plot2_program2.png)