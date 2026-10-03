# Solution

## 1. Observation

Suppose we decide to execute two adjacent opportunities `u` and `v`.

Exactly one of them executes first.

- If `u` executes before `v`, then `v` loses `C[u,v]`.
- If `v` executes before `u`, then `u` loses `C[v,u]`.

Therefore, for every edge whose two endpoints are both selected, we may orient the edge from the opportunity executed earlier to the opportunity executed later.

If an opportunity is skipped, it never executes and therefore never creates market impact. Consequently, edges incident to skipped vertices are irrelevant.

For a selected vertex `i`, its profit when it executes is

[
P_i - \sum_{\substack{j\text{ selected neighbor of }i\\j\text{ executes before }i}} C_{j,i}.
]

The vertex is executable exactly when this value is strictly positive.

Thus the problem becomes:

1. choose a subset of vertices;
2. orient every edge whose endpoints are both selected;
3. require every selected vertex to have positive profit after all incoming impacts;
4. require the orientation to correspond to some execution order.

The last condition means that the orientation must be acyclic.

---

## 2. Why paths are easy

For a path, every orientation is acyclic.

So after selecting the vertices and orienting the active edges, a valid execution order always exists: take any topological ordering of the resulting directed forest.

This allows us to process the path from left to right.

When processing vertex `i`, only two edges can affect it:

- `(i-1, i)`;
- `(i, i+1)`.

Once the decision for `(i, i+1)` is made, the final profit of vertex `i` is known forever.

Therefore only constant-size state is necessary.

---

## 3. Path DP

While processing vertex `i`, use three states.

### State 0

Vertex `i` is skipped.

Because it never executes, it creates no market impact.

### State 1

Vertex `i` is selected and receives no impact from its left neighbor.

### State 2

Vertex `i` is selected and receives the impact

[ C_{i-1,i}] from its left neighbor.

Let [dp[s]]be the maximum number of selected vertices so far when the current vertex has state `s`.

Importantly, a selected current vertex is not validated immediately. We wait until the relation with its right neighbor is known.

---

## 4. Transitions

Consider edge `(i, i+1)`.

Let

\[A_i = C_{i,i+1}\] and \[ B_i = C_{i+1,i} \]

Assume vertex `i` has already received left-side penalty `L`.

There are several possibilities.

### Skip `i+1`

If `i` is selected, its final profit is

\[
P_i-L.
\]

Therefore this transition is valid when

\[
P_i-L>0.
\]

The next state is `0`.

If `i` itself was skipped, no profitability check is needed.

---

### `i` is skipped and `i+1` is selected

The edge is inactive because `i` never executes.

Therefore `i+1` receives no impact from the left and enters state `1`.

---

### Both vertices are selected and `i` executes first

The orientation is

\[
i \rightarrow i+1.
\]

Vertex `i` receives no right-side penalty, so we require

\[
P_i-L>0.
\]

Vertex `i+1` receives `A_i`, so it enters state `2`.

---

### Both vertices are selected and `i+1` executes first

The orientation is

\[
i+1 \rightarrow i.
\]

Now vertex `i` additionally receives `B_i`, so we require

\[
P_i-L-B_i>0.
\]

Vertex `i+1` receives no impact from `i`, so it enters state `1`.

---

## 5. Final vertex

After all path edges have been processed, vertex `N-1` has no undecided right neighbor.

If it is skipped, the state is automatically valid.

If it is selected in state `1`, we require

\[
P_{N-1}>0.
\]

If it is selected in state `2`, we require

\[
P_{N-1}-C_{N-2,N-1}>0.
\]

The largest valid DP value is the answer.

---

## 6. Why skipped vertices matter

A skipped opportunity must not be treated as if it participates in an execution ordering.

For example:

```text
3 0
1 -100 1
100 100
100 100
```

Opportunity `2` can never execute.

However, by skipping it, opportunities `1` and `3` can both execute.

The answer is therefore `2`.

This is why the DP contains an explicit skipped state. An edge has an orientation only when both of its endpoints are selected.

---

## 7. Handling a cycle

A cycle introduces one additional issue.

Unlike a path, an orientation of a cycle is not always acyclic.

For a simple cycle, a directed cycle occurs only when:

- every vertex is selected, and
- every edge is oriented consistently around the entire cycle.

If at least one vertex is skipped, the selected graph is a collection of paths and is automatically acyclic.

We handle the cycle by considering the status of vertex `0` and vertex `N-1`.

There are four cases.

---

### Case A: vertex `0` is skipped

The closing edge `(N-1,0)` is inactive.

The remaining graph behaves like a path.

---

### Case B: vertex `0` is selected and vertex `N-1` is skipped

Again, the closing edge is inactive.

We run the path DP with these endpoint conditions fixed.

---

### Case C: both endpoints are selected and `N-1` executes before `0`

The closing edge is

\[
N-1 \rightarrow 0.
\]

Therefore vertex `0` receives

\[
C_{N-1,0}.
\]

There is exactly one forbidden internal orientation:

\[
0\rightarrow1\rightarrow2\rightarrow\cdots\rightarrow N-1.
\]

Together with

\[
N-1\rightarrow0,
\]

this would form a directed cycle.

During the DP we keep one extra boolean flag indicating whether we have already broken this forbidden pattern.

Skipping any vertex or orienting any internal edge in the opposite direction makes the orientation safe.

At the end, the state where the entire forbidden pattern remains intact is rejected.

---

### Case D: both endpoints are selected and `0` executes before `N-1`

Now the closing edge is

\[
0\rightarrow N-1.
\]

Vertex `N-1` receives

\[
C_{0,N-1}.
\]

The forbidden internal orientation is the reverse chain:

\[
0\leftarrow1\leftarrow2\leftarrow\cdots\leftarrow N-1.
\]

Together with the closing edge, this would again form a directed cycle.

We track and reject exactly this orientation in the same way.

The answer for a cycle is the maximum over these four cases.

---

## 8. Correctness Proof

We prove that the algorithm returns the maximum possible number of executable opportunities.

### Lemma 1

For any chosen subset of opportunities and any execution order, orienting each active edge from the earlier executed endpoint to the later executed endpoint gives an acyclic orientation.

#### Proof

Every directed edge points from an earlier opportunity to a later opportunity in the execution order.

A directed cycle would require an opportunity to occur earlier than itself, which is impossible.

Therefore the orientation is acyclic. ∎

---

### Lemma 2

For any acyclic orientation of the active edges satisfying every selected vertex's profit constraint, there exists a valid execution order.

#### Proof

Every directed acyclic graph has a topological ordering.

Execute the selected opportunities in that topological order.

For every directed edge `u -> v`, `u` executes before `v`, so exactly the corresponding impact `C[u,v]` is applied to `v`.

The assumed profit constraints therefore guarantee that every selected opportunity has strictly positive profit when it executes. ∎

---

### Lemma 3

The path DP considers every possible valid choice involving vertices `0..i`.

#### Proof

For every current vertex, exactly three relevant situations exist:

1. it is skipped;
2. it is selected and its left neighbor does not execute before it;
3. it is selected and its left neighbor executes before it.

These are precisely states `0`, `1`, and `2`.

For the right neighbor, the DP considers every possible choice:

- skip it;
- select it after the current vertex;
- select it before the current vertex.

Thus every possible selection and orientation of the path is represented. ∎

---

### Lemma 4

Whenever the DP moves past vertex `i`, it checks exactly the complete profit constraint of `i`.

#### Proof

Vertex `i` has at most two neighbors.

Its left-side impact is already known from the current state.

The transition determines whether its right neighbor is skipped, executes after `i`, or executes before `i`.

Therefore after the transition, every possible incoming impact to `i` is known.

The DP accepts the transition exactly when the resulting profit is strictly positive. ∎

---

### Lemma 5

Every orientation accepted by the path DP corresponds to a valid execution order.

#### Proof

After skipped vertices are removed, the active graph is a collection of paths.

A path contains no undirected cycle, so any orientation of it is acyclic.

By Lemma 2, the orientation therefore has a valid execution order. ∎

---

### Lemma 6

The cycle algorithm rejects exactly the orientations that cannot correspond to an execution order.

#### Proof

If any vertex is skipped, the cycle is broken into paths, so no directed cycle is possible.

If every vertex is selected, the only way to obtain a directed cycle is for every edge to point consistently around the original cycle.

There are exactly two such orientations: clockwise and counterclockwise.

Cases C and D each fix one direction of the closing edge and explicitly reject the corresponding consistent orientation.

All other orientations are acyclic. ∎

---

### Theorem

The algorithm outputs the maximum possible number of successfully executed opportunities.

#### Proof

By Lemmas 3 and 4, the DP considers every possible selection/orientation and accepts only selections satisfying all profit constraints.

By Lemmas 5 and 6, it accepts exactly those orientations that correspond to valid execution orders.

Therefore every value considered by the algorithm is achievable.

Conversely, by Lemma 1, every valid execution sequence produces an acyclic orientation represented by one of the DP cases. Hence no feasible solution is omitted.

Taking the maximum therefore gives the optimal number of executed opportunities. ∎

---

## 9. Complexity

The DP has only a constant number of states per vertex.

Each path transition performs constant work.

For a path, the time complexity is

\[
O(N).
\]

For a cycle, we run a constant number of path-DP cases, so the total time remains

\[
O(N).
\]

The DP itself uses only a constant number of states at a time, giving

\[
O(1)
\]

auxiliary DP memory.
The input arrays require
[O(N)]

memory overall.