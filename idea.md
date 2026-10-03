# Problem Idea — Vanishing Arbitrage

## Initial Concept

I wanted to design a competitive programming problem based on a situation from quantitative trading rather than starting from a standard graph or dynamic programming template.

The initial idea came from fragmented-market arbitrage.

Suppose several arbitrage opportunities exist at the same time. They are not completely independent: two opportunities may depend on the same market liquidity. Executing one trade changes that market, so an opportunity that appears profitable now may disappear before it can be executed.

The central question became:

> If executing one arbitrage permanently changes the profitability of neighboring arbitrages, what is the largest number of opportunities that can actually be executed?

The goal was to make execution order part of the combinatorial problem.

---

## Rejected Variant 1: Shared Collateral / Margin Cascade

The first finance-based idea used positions sharing a collateral pool.

Each position had a liquidation threshold, and liquidating one position changed the amount of collateral available to the others.

This was rejected because the underlying structure became too similar to existing resource-scheduling and threshold-selection problems. The financial story was different, but the algorithmic problem was not distinctive enough.

---

## Rejected Variant 2: Two-Level Liquidity

The next idea used triangular arbitrage opportunities sharing markets.

Every shared market had two liquidity states:

- fresh liquidity;
- depleted liquidity.

The first arbitrage using a market received its fresh value. Later arbitrages received the depleted value.

For a selected set of opportunities, this led to an expression of the form

\[
\sum_i B_i - \sum_{(i,j)} L_{ij},
\]

where \(B_i\) was the fresh profit of opportunity \(i\) and \(L_{ij}\) was the deterioration caused when two neighboring opportunities were both executed.

Although execution order affected whether individual trades remained profitable, the total value of a selected set was largely independent of the order.

This reduced too naturally to a weighted graph-selection problem, so I did not use this version.

---

## Rejected Variant 3: Winner-Takes-All Shared Liquidity

I then considered making shared liquidity disappear completely.

For every shared liquidity pocket, whichever neighboring arbitrage executed first would capture its value.

This produced a useful observation: an execution order induces an orientation of the interaction graph.

For example,

\[
A \rightarrow B
\]

could mean that \(A\) executes before \(B\) and therefore captures their shared liquidity.

However, this version became close to a weighted edge-orientation problem: orient edges and determine which vertices satisfy a local weight constraint.

The transformation was interesting, but the underlying problem felt more familiar than I wanted.

---

## Rejected Variant 4: Explicit Liquidity Capacities

Another possibility was to give each shared market an integer amount of liquidity and let each arbitrage consume some quantity.

This made the model more realistic, but introduced large resource states. Depending on the exact rule, the problem began resembling knapsack or general resource-constrained scheduling.

It also made the statement substantially more complicated.

I wanted the final problem to have a small statement and a non-obvious solution rather than a large simulation state.

---

## Final Idea: Asymmetric Permanent Market Impact

The final version models the effect of one arbitrage on another directly.

Each arbitrage opportunity \(i\) has an initial profit \(p_i\).

Opportunities form a path or a cycle. Two adjacent opportunities interact because they share a market.

The interaction is asymmetric.

If opportunity \(i\) executes before opportunity \(j\), then \(j\)'s profit is permanently reduced by

\[
c_{i,j}.
\]

Executing \(j\) before \(i\) may cause a completely different reduction

\[
c_{j,i}.
\]

Therefore, in general,

\[
c_{i,j} \neq c_{j,i}.
\]

This represents different trade sizes, directions, slippage, and market impact.

An opportunity can only be executed when its current profit is strictly positive.

Opportunities may also be skipped.

The objective is to maximize the number of opportunities that can successfully execute.

---

## Key Observation

At first, the problem appears to require trying execution orders.

For \(k\) selected opportunities, there may be \(k!\) possible orders.

However, for two adjacent selected opportunities, only their relative order matters.

If

\[
i \rightarrow j,
\]

then \(i\) executes before \(j\), and \(j\) receives the corresponding market-impact penalty.

Thus an execution order can be represented as an orientation of the edges between selected opportunities.

For a selected opportunity \(i\), its realized profit is

\[
p_i -
\sum_{\substack{j\text{ adjacent to }i\\j\text{ executes before }i}}
c_{j,i}.
\]

It is executable exactly when this value is strictly positive.

This turns a global permutation problem into local decisions on graph edges.

---

## Why Paths Are Special

On a path, every orientation is acyclic.

Therefore every set of local precedence decisions corresponds to at least one valid global execution order.

When processing the path from left to right, after deciding the relation between \(i\) and \(i+1\), all information affecting opportunity \(i\) is known.

Nothing farther to the right can change its realized profit.

This allows the problem to be solved using a constant number of dynamic-programming states per position.

The apparent factorial search over execution orders therefore collapses to linear time.

---

## Why Cycles Are Different

A cycle introduces one additional global condition.

The local decisions

\[
1\rightarrow2,\quad
2\rightarrow3,\quad
\ldots,\quad
n\rightarrow1
\]

may make every individual opportunity appear valid, but they require

\[
1<2<\cdots<n<1,
\]

which cannot correspond to any execution order.

The reverse directed cycle is impossible for the same reason.

If at least one opportunity is skipped, however, the cycle is broken into paths and this obstruction disappears.

This creates an important distinction between local profitability and global executability.

---

## Intended Difficulty

The intended difficulty comes from recognizing several transformations:

1. Trying execution permutations directly is infeasible.
2. Only the relative order of adjacent opportunities matters.
3. Relative execution order can be represented by edge directions.
4. Profitability of a vertex depends only on its two incident decisions.
5. On paths, all orientations are globally realizable.
6. Cycles require additionally excluding a complete directed cycle.
7. These observations allow a constant-state dynamic program.

The intended solution runs in \(O(n)\) time.

---

## Why I Chose This Version

I chose this version because the financial interpretation and the algorithmic structure reinforce each other.

The market-impact rule explains naturally why execution order matters, while asymmetric impact prevents the problem from reducing to simply assigning one fixed shared value.

At the same time, limiting the interaction graph to paths and cycles prevents the ordering problem from becoming an unrestricted graph problem.

The result is a problem that initially looks like an execution simulation or permutation search but reduces to a small dynamic program after identifying the correct representation.
