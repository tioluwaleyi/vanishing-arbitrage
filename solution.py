import sys

NEG = -10**9


def solve_instance(n, t, p, edges):
    """
    State for the current vertex i:

      0 = i is skipped
      1 = i is selected and receives no impact from i-1
      2 = i is selected and receives impact A[i-1] from i-1

    If i is selected, we postpone checking its final profitability
    until we decide what happens on edge (i, i+1).

    This gives O(N) time and O(1) auxiliary memory.
    """

    if n == 1:
        return 1 if p[0] > 0 else 0

    def run_path(
        first_selected=None,
        last_selected=None,
        initial_penalty=0,
        final_penalty=0,
        forbidden_direction=None,
    ):
        """
        Solve the chain 0 -- 1 -- ... -- n-1.

        first_selected:
            None -> either
            0    -> force vertex 0 skipped
            1    -> force vertex 0 selected

        last_selected:
            None -> either
            0    -> force vertex n-1 skipped
            1    -> force vertex n-1 selected

        initial_penalty:
            external penalty already received by vertex 0.

        final_penalty:
            external penalty received by vertex n-1.

        forbidden_direction:
            None
            "forward"
            "backward"

        For a cycle with both endpoints selected, `safe` records
        whether we have already broken the one forbidden directed
        full-cycle orientation.
        """

        # dp[state][safe] = maximum selected count
        dp = [[NEG, NEG] for _ in range(3)]

        if first_selected is None:
            # Skip vertex 0.
            dp[0][1 if forbidden_direction else 0] = 0

            # Select vertex 0.
            dp[1][0] = 1

        elif first_selected == 0:
            dp[0][1 if forbidden_direction else 0] = 0

        else:
            dp[1][0] = 1

        # Process edges (i, i+1).
        for i in range(n - 1):
            a, b = edges[i]

            # a = C_{i, i+1}
            # b = C_{i+1, i}

            new_dp = [[NEG, NEG] for _ in range(3)]

            for state in range(3):
                for safe in range(2):
                    value = dp[state][safe]

                    if value < 0:
                        continue

                    # Impact already received by current vertex i
                    # from its left side.
                    if state == 0:
                        left_penalty = 0
                    elif i == 0:
                        left_penalty = initial_penalty
                    elif state == 2:
                        left_penalty = edges[i - 1][0]
                    else:
                        left_penalty = 0

                    # -----------------------------------------
                    # Option 1: skip vertex i+1
                    # -----------------------------------------
                    #
                    # If current i is selected, its profit is now
                    # final because the skipped next vertex cannot
                    # affect it.
                    if state == 0 or p[i] - left_penalty > 0:
                        next_safe = 1 if forbidden_direction else safe

                        if value > new_dp[0][next_safe]:
                            new_dp[0][next_safe] = value

                    # -----------------------------------------
                    # Option 2: select vertex i+1
                    # -----------------------------------------

                    if state == 0:
                        # Current vertex is skipped.
                        #
                        # Therefore edge (i, i+1) is inactive.
                        # The new selected vertex receives no impact
                        # from the left.
                        next_safe = 1 if forbidden_direction else safe

                        if value + 1 > new_dp[1][next_safe]:
                            new_dp[1][next_safe] = value + 1

                    else:
                        # Both i and i+1 are selected.

                        # -------------------------------------
                        # i executes before i+1
                        # -------------------------------------
                        #
                        # i receives no impact from the right.
                        # i+1 receives impact a.
                        if p[i] - left_penalty > 0:
                            next_safe = safe

                            # If the forbidden full-cycle orientation
                            # is backward, a forward edge breaks it.
                            if forbidden_direction == "backward":
                                next_safe = 1

                            if value + 1 > new_dp[2][next_safe]:
                                new_dp[2][next_safe] = value + 1

                        # -------------------------------------
                        # i+1 executes before i
                        # -------------------------------------
                        #
                        # i receives impact b from the right.
                        # i+1 receives no impact from i.
                        if p[i] - left_penalty - b > 0:
                            next_safe = safe

                            # If the forbidden full-cycle orientation
                            # is forward, a backward edge breaks it.
                            if forbidden_direction == "forward":
                                next_safe = 1

                            if value + 1 > new_dp[1][next_safe]:
                                new_dp[1][next_safe] = value + 1

            dp = new_dp

        # Finalize vertex n-1.
        answer = NEG

        for state in range(3):
            selected = state != 0

            if last_selected is not None:
                if selected != bool(last_selected):
                    continue

            for safe in range(2):
                value = dp[state][safe]

                if value < 0:
                    continue

                # In the cycle cases, safe=False means:
                #
                # every vertex was selected AND every internal edge
                # followed the forbidden direction.
                #
                # Together with the fixed closing edge, that creates
                # a directed cycle and cannot correspond to any
                # execution order.
                if forbidden_direction is not None and not safe:
                    continue

                if not selected:
                    valid = True

                else:
                    if state == 2:
                        left_penalty = edges[n - 2][0]
                    else:
                        left_penalty = 0

                    valid = (
                        p[n - 1]
                        - left_penalty
                        - final_penalty
                        > 0
                    )

                if valid:
                    answer = max(answer, value)

        return answer

    # =========================================================
    # PATH
    # =========================================================

    if t == 0:
        return run_path()

    # =========================================================
    # CYCLE
    # =========================================================

    closing_a, closing_b = edges[n - 1]

    # Closing edge is (n-1, 0):
    #
    # closing_a = C_{n-1, 0}
    # closing_b = C_{0, n-1}

    answer = 0

    # ---------------------------------------------------------
    # Case A: vertex 0 skipped
    # ---------------------------------------------------------
    #
    # Closing edge is inactive. The remaining selected graph
    # is simply a collection of paths.
    answer = max(
        answer,
        run_path(
            first_selected=0,
            last_selected=None,
        ),
    )

    # ---------------------------------------------------------
    # Case B: vertex 0 selected, vertex n-1 skipped
    # ---------------------------------------------------------
    #
    # Again the closing edge is inactive.
    answer = max(
        answer,
        run_path(
            first_selected=1,
            last_selected=0,
        ),
    )

    # ---------------------------------------------------------
    # Case C: both endpoints selected, n-1 executes before 0
    # ---------------------------------------------------------
    #
    # Vertex 0 receives closing_a.
    #
    # If every internal edge is also forward:
    #
    #   0 -> 1 -> 2 -> ... -> n-1 -> 0
    #
    # we obtain a directed cycle, which is impossible.
    answer = max(
        answer,
        run_path(
            first_selected=1,
            last_selected=1,
            initial_penalty=closing_a,
            final_penalty=0,
            forbidden_direction="forward",
        ),
    )

    # ---------------------------------------------------------
    # Case D: both endpoints selected, 0 executes before n-1
    # ---------------------------------------------------------
    #
    # Vertex n-1 receives closing_b.
    #
    # If every internal edge is backward:
    #
    #   0 <- 1 <- 2 <- ... <- n-1
    #
    # together with 0 -> n-1, we obtain the reverse directed
    # cycle, which must also be rejected.
    answer = max(
        answer,
        run_path(
            first_selected=1,
            last_selected=1,
            initial_penalty=0,
            final_penalty=closing_b,
            forbidden_direction="backward",
        ),
    )

    return answer


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

    print(solve_instance(n, t, p, edges))


if __name__ == "__main__":
    solve()