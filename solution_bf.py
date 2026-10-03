import sys
from itertools import combinations, permutations


def build_graph(n, t, edges):
    """
    adj[u] contains (v, impact_uv), where impact_uv is the
    amount subtracted from v if u executes before v.
    """
    adj = [[] for _ in range(n)]

    # Path edges: (0,1), (1,2), ..., (n-2,n-1)
    for i in range(n - 1):
        a, b = edges[i]

        # i executes before i+1
        adj[i].append((i + 1, a))

        # i+1 executes before i
        adj[i + 1].append((i, b))

    # Closing edge for a cycle: (n-1, 0)
    if t == 1:
        a, b = edges[n - 1]

        # n-1 executes before 0
        adj[n - 1].append((0, a))

        # 0 executes before n-1
        adj[0].append((n - 1, b))

    return adj


def order_is_valid(order, p, adj):
    """
    Check whether exactly the vertices in `order` can execute
    successfully in this execution order.

    Only selected/executed vertices matter. Skipped vertices never
    execute, so they never apply market impact.
    """
    selected = set(order)
    current = p[:]

    for u in order:
        if current[u] <= 0:
            return False

        # u has now executed. Its impact applies only to selected
        # neighbors that have not executed yet.
        selected.remove(u)

        for v, impact in adj[u]:
            if v in selected:
                current[v] -= impact

    return True


def brute_force(n, t, p, edges):
    adj = build_graph(n, t, edges)
    vertices = range(n)

    # Try larger subsets first. As soon as one is feasible,
    # its size is optimal.
    for size in range(n, 0, -1):
        for subset in combinations(vertices, size):
            for order in permutations(subset):
                if order_is_valid(order, p, adj):
                    return size

    return 0


def solve():
    data = sys.stdin.buffer.read().split()

    if not data:
        return

    it = iter(data)

    n = int(next(it))
    t = int(next(it))

    p = [int(next(it)) for _ in range(n)]

    edge_count = n if t == 1 else n - 1
    edges = []

    for _ in range(edge_count):
        a = int(next(it))
        b = int(next(it))
        edges.append((a, b))

    print(brute_force(n, t, p, edges))


if __name__ == "__main__":
    solve()