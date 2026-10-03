# Vanishing Arbitrage

## Problem Statement

A quantitative trading system has detected \(N\) short-lived arbitrage opportunities across a fragmented market.

The opportunities are arranged in their **interaction order**. Each opportunity interacts only with the opportunity immediately before it and immediately after it.

The interaction structure is either:

- a **path**, where opportunity \(1\) interacts with \(2\), \(2\) with \(3\), and so on; or
- a **cycle**, where the same interactions exist and opportunities \(N\) and \(1\) also interact.

Each opportunity \(i\) initially has profit \(P_i\).

Two adjacent opportunities share a market. Executing one of them permanently moves that market and reduces the profit of the other opportunity if the other opportunity has not yet executed.

Market impact is **asymmetric**.

For every interaction between opportunities \(u\) and \(v\):

- if \(u\) executes before \(v\), the profit of \(v\) is reduced by \(C_{u,v}\);
- if \(v\) executes before \(u\), the profit of \(u\) is reduced by \(C_{v,u}\).

The two values do not have to be equal.

An opportunity may be executed only if its **current profit is strictly positive**.

You may execute the opportunities in any order, and you may choose not to execute some opportunities.

Once an opportunity has executed, later market movements do not affect it.

Determine the maximum number of opportunities that can be successfully executed.

---

## Detailed Rules

Initially, the current profit of opportunity \(i\) is

\[
P_i.
\]

Suppose opportunities \(u\) and \(v\) are adjacent.

If \(u\) is executed while \(v\) has not yet been executed, then \(v\)'s current profit decreases by

\[
C_{u,v}.
\]

Similarly, if \(v\) is executed while \(u\) has not yet been executed, then \(u\)'s current profit decreases by

\[
C_{v,u}.
\]

If an opportunity is never executed, its final profit does not matter.

An opportunity whose current profit is zero or negative cannot be executed.

All market impacts are permanent.

---

## Input

The first line contains two integers:

```text
N T
```

where:

- \(N\) is the number of arbitrage opportunities;
- \(T\) describes the interaction structure:
  - \(T=0\): the opportunities form a path;
  - \(T=1\): the opportunities form a cycle.

The second line contains \(N\) integers:

```text
P1 P2 ... PN
```

where \(P_i\) is the initial profit of opportunity \(i\).

For a path, the next \(N-1\) lines describe the interactions

\[
(1,2),(2,3),\ldots,(N-1,N).
\]

For a cycle, the next \(N\) lines describe

\[
(1,2),(2,3),\ldots,(N-1,N),(N,1).
\]

The line describing an interaction between \(u\) and \(v\) contains two integers:

```text
A B
```

where:

- \(A=C_{u,v}\), the reduction applied to \(v\) if \(u\) executes first;
- \(B=C_{v,u}\), the reduction applied to \(u\) if \(v\) executes first.

The interaction lines are given in the order described above.

---

## Output

Print one integer: the maximum number of arbitrage opportunities that can be successfully executed.

---

## Constraints

\[
1 \le N \le 2\cdot10^5
\]

\[
-10^9 \le P_i \le 10^9
\]

\[
0 \le C_{u,v} \le 10^9
\]

For \(T=1\),

\[
N\ge3.
\]

All values are integers.

---

## Example 1

Input

```text
4 0
5 4 7 3
6 1
2 5
4 1
```

 Output

```text
4
```

### Explanation

The opportunities form the path

```text
1 -- 2 -- 3 -- 4
```

Consider executing them in the order

```text
2, 1, 4, 3
```

Opportunity \(2\) executes with profit \(4\).

Its execution reduces opportunity \(1\)'s profit by \(1\) and opportunity \(3\)'s profit by \(2\).

Opportunity \(1\) therefore executes with profit

\[
5-1=4>0.
\]

Opportunity \(4\) then executes with profit \(3\). Because opportunity \(3\) has not executed yet, this reduces opportunity \(3\)'s profit by \(1\).

Opportunity \(3\) now has profit

\[
7-2-1=4>0.
\]

Therefore all four opportunities can be executed.

The answer is \(4\).

---

## Example 2

 Input

```text
3 0
1 1 1
2 2
2 2
```

 Output

```text
2
```

Explanation

The opportunities form

```text
1 -- 2 -- 3
```

Every opportunity initially has profit \(1\).

Any execution across an interaction reduces the later opportunity's profit by \(2\).

It is impossible to execute all three opportunities.

For example, executing opportunity \(2\) first makes both opportunities \(1\) and \(3\) unprofitable.

However, opportunities \(1\) and \(3\) are not adjacent, so they can both be executed successfully.

Thus the maximum is \(2\).

---

## Example 3

Input

```text
3 1
1 1 1
1 1
1 1
1 1
```

 Output

```text
2
```

 Explanation

The opportunities form a cycle.

Because execution requires **strictly positive** profit, an opportunity that receives an impact of \(1\) has profit

\[
1-1=0
\]

and cannot execute.

It is possible to execute two opportunities by choosing an appropriate order, but executing all three is impossible.

Therefore the answer is \(2\).

---

## Notes

The execution order itself does not need to be printed.

Only the maximum possible number of successfully executed opportunities is required.

An opportunity with initial profit \(P_i\le0\) may still be present in the input, but it cannot execute unless the rules of the problem permit it to have positive profit at its execution time. Since market impacts only decrease profits, such an opportunity can never become executable.

All comparisons with profitability are strict:

\[
\text{current profit} > 0.
\]
