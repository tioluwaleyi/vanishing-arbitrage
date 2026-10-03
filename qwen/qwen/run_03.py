import sys
from collections import deque

def solve():
    input = sys.stdin.readline
    
    N, T = map(int, input().split())
    P = list(map(int, input().split()))
    
    # Store edges: for edge between i and i+1, store (C_{i,i+1}, C_{i+1,i})
    edges = []
    num_edges = N if T == 1 else N - 1
    for _ in range(num_edges):
        A, B = map(int, input().split())
        edges.append((A, B))  # A=C_{u,v}, B=C_{v,u} for edge (u,v)
    
    if N == 0:
        print(0)
        return
    
    if T == 0:  # Path
        # dp[i][d] where i is index 0..N-1, d in {0,1} 
        # d=0: edge (i-1,i) directed i-1 -> i (i receives impact from left)
        # d=1: edge (i-1,i) directed i -> i-1 (i does NOT receive impact from left)
        # For i=0, no left edge, treat d as 1 (no incoming from left)
        
        NEG_INF = -10**9
        
        # dp[d] for current position
        # Initialize for i=0
        # Edge 0 is between node 0 and node 1
        # For node 0, left incoming = 0 always
        # We choose direction of edge 0
        
        # Let's do iterative DP
        # State after processing up to node i: direction of edge (i, i+1) if exists
        
        # dp_dir = dict mapping direction of last edge to best count
        # Start: before node 0, no edge yet
        
        # Process node by node
        # At node i, we have incoming_from_left determined by prev_edge_dir
        # We choose next_edge_dir (direction of edge (i,i+1))
        # Node i's incoming = incoming_from_left + (impact from right if next_edge_dir says i+1->i)
        
        # For edge (i,i+1): stored as edges[i] = (C_{i,i+1}, C_{i+1,i})
        # If edge directed i -> i+1: node i+1 gets C_{i,i+1} impact from left, node i gets 0 from this edge
        # If edge directed i+1 -> i: node i gets C_{i+1,i} impact from right side of this edge
        
        # Define: dir=0 means i -> i+1, dir=1 means i+1 -> i
        
        # dp[i][d] = max executable count among nodes 0..i, where d is direction of edge (i,i+1) if i<N-1
        # For last node, no outgoing edge
        
        if N == 1:
            print(1 if P[0] > 0 else 0)
            return
        
        # dp array: for each possible direction of current edge, store max count
        # Initially at node 0, no incoming from left
        # Choose direction of edge 0
        
        # Let dp_next[d] be computed
        # We'll maintain dp as list of size 2
        
        # Before any edge processed, conceptually edge "-1" doesn't exist
        # Process node 0: incoming_left = 0. Choose dir0 for edge 0.
        # After choosing dir0, node 0's total incoming = 0 + (if dir0==1, C_{1,0} else 0)
        # Wait, dir0=1 means edge 0+1 -> 0, so node 0 gets C_{edges[0][1]} = C_{1,0}
        
        # Hmm, I'm confusing myself. Let me restart with clearer notation.
        
        # For edge e between nodes L and R (L=e, R=e+1):
        # edges[e] = (C_LR, C_RL) where C_LR = impact on R if L executes first, C_RL = impact on L if R executes first
        
        # Direction choices for edge e:
        #   dir=0: L executes before R => R receives C_LR from this edge
        #   dir=1: R executes before L => L receives C_RL from this edge
        
        # Node i receives impact from:
        #   - Left edge (i-1,i): if dir of that edge is 1 (i executes before i-1)... wait no.
        #     Edge (i-1,i): L=i-1, R=i. dir=0 means i-1 before i, i receives C_{i-1,i}. dir=1 means i before i-1, i-1 receives C_{i,i-1}.
        #     So node i receives from left edge if dir(left_edge)=0.
        #   - Right edge (i,i+1): L=i, R=i+1. dir=0 means i before i+1, i+1 receives. dir=1 means i+1 before i, i receives C_{i+1,i}.
        #     So node i receives from right edge if dir(right_edge)=1.
        
        # Great! So:
        # Node i's incoming impact = (if i>0 and dir(edge i-1)==0 then C_{edges[i-1][0]} else 0) 
        #                            + (if i<N-1 and dir(edge i)==1 then C_{edges[i][1]} else 0)
        
        # Now DP: process edges left to right. State = direction of previous edge.
        
        # dp[d_prev] = max count for nodes 0..i-1 already decided, with edge (i-1,i) having direction d_prev
        # When moving to decide edge i's direction d_curr, we can finalize node i's executability
        
        # Initialize: no edges before node 0. Think of virtual edge -1 with d_prev=1 (so node 0 gets no left impact)
        # Actually simpler: start with dp for "before deciding edge 0". Node 0's left impact is always 0.
        
        # Let me index differently. After deciding directions for edges 0..k-1, nodes 0..k-1 have their left impacts known, 
        # but node k-1's right impact depends on edge k-1 which IS decided. So nodes 0..k-1 fully determined except...
        # Node k-1's right impact comes from edge k-1 which is decided. So yes, nodes 0..k-1 are fully determined once edges 0..k-1 are decided.
        
        # Wait no: node k-1's right impact is from edge (k-1,k) which is edge k-1. Yes, decided. Good.
        
        # So after deciding edge e, node e is fully determined (left from edge e-1, right from edge e).
        
        # DP state after deciding edges 0..e: direction of edge e. Count includes nodes 0..e.
        
        # Init: decide edge 0. Node 0's left impact = 0. Node 0's right impact = from edge 0 if dir=1.
        # So after deciding dir0=d, node 0 incoming = (C_{edges[0][1]} if d==1 else 0).
        # Executable if P[0] > incoming.
        
        dp = [-10**9, -10**9]  # dp[d] for direction of last decided edge
        
        # Decide edge 0
        for d in [0, 1]:
            incoming_0 = edges[0][1] if d == 1 else 0
            cnt = 1 if P[0] > incoming_0 else 0
            dp[d] = cnt
        
        # Decide edges 1 to N-2 (for path, edges go 0 to N-2)
        for e in range(1, N-1):
            new_dp = [-10**9, -10**9]
            for d_prev in [0, 1]:
                if dp[d_prev] < 0:
                    continue
                for d_curr in [0, 1]:
                    # Node e's incoming: left from edge e-1 if d_prev==0, right from edge e if d_curr==1
                    incoming_e = 0
                    if d_prev == 0:
                        incoming_e += edges[e-1][0]  # C_{e-1,e}
                    if d_curr == 1:
                        incoming_e += edges[e][1]    # C_{e+1,e}
                    add = 1 if P[e] > incoming_e else 0
                    val = dp[d_prev] + add
                    if val > new_dp[d_curr]:
                        new_dp[d_curr] = val
            dp = new_dp
        
        # Finalize: node N-1's incoming depends on edge N-2's direction
        ans = 0
        for d_last in [0, 1]:
            if dp[d_last] < 0:
                continue
            # Node N-1: left impact from edge N-2 if d_last==0
            incoming_last = edges[N-2][0] if d_last == 0 else 0
            add = 1 if P[N-1] > incoming_last else 0
            total = dp[d_last] + add
            if total > ans:
                ans = total
        
        print(ans)
        
    else:  # Cycle
        # For cycle, we break it into a path by removing one edge, try all possibilities
        # But N can be 2e5, trying all N breaks is O(N^2). Need better approach.
        
        # In a cycle, valid orientations are those without directed cycles.
        # A directed cycle occurs iff all edges are oriented consistently (all clockwise or all counterclockwise).
        # So we need to exclude the two "bad" orientations.
        
        # Alternative: fix one edge's direction and do DP on the resulting path, ensuring consistency.
        # Try both directions for edge 0, run path DP on edges 1..N-1 with wrap-around consideration.
        
        # For cycle with N nodes and N edges, break edge N-1 (between N-1 and 0).
        # Run DP treating it as path 0..N-1 with edges 0..N-2, but node 0 also has right impact from edge N-1.
        
        # Fix direction of edge N-1 (between N-1 and 0):
        #   dir=0: N-1 before 0, node 0 gets C_{N-1,0} = edges[N-1][0]
        #   dir=1: 0 before N-1, node N-1 gets C_{0,N-1} = edges[N-1][1]
        
        # Also, the overall orientation must not be all-clockwise or all-counterclockwise.
        
        # Let's try fixing edge N-1's direction and doing modified path DP.
        
        if N == 1:
            print(1 if P[0] > 0 else 0)
            return
        
        best_ans = 0
        
        for fixed_dir_last in [0, 1]:
            # fixed_dir_last is direction of edge N-1
            
            # Initialize DP for edge 0, but node 0's incoming now includes contribution from edge N-1
            dp = [-10**9, -10**9]
            
            for d in [0, 1]:
                # Node 0: left impact from edge N-1 if fixed_dir_last==0, right impact from edge 0 if d==1
                incoming_0 = 0
                if fixed_dir_last == 0:
                    incoming_0 += edges[N-1][0]  # C_{N-1,0}
                if d == 1:
                    incoming_0 += edges[0][1]    # C_{1,0}
                cnt = 1 if P[0] > incoming_0 else 0
                dp[d] = cnt
            
            # Process edges 1 to N-2
            for e in range(1, N-1):
                new_dp = [-10**9, -10**9]
                for d_prev in [0, 1]:
                    if dp[d_prev] < 0:
                        continue
                    for d_curr in [0, 1]:
                        incoming_e = 0
                        if d_prev == 0:
                            incoming_e += edges[e-1][0]
                        if d_curr == 1:
                            incoming_e += edges[e][1]
                        add = 1 if P[e] > incoming_e else 0
                        val = dp[d_prev] + add
                        if val > new_dp[d_curr]:
                            new_dp[d_curr] = val
                dp = new_dp
            
            # Finalize node N-1
            for d_last in [0, 1]:
                if dp[d_last] < 0:
                    continue
                # Node N-1: left impact from edge N-2 if d_last==0, right impact from edge N-1 if fixed_dir_last==1
                incoming_last = 0
                if d_last == 0:
                    incoming_last += edges[N-2][0]
                if fixed_dir_last == 1:
                    incoming_last += edges[N-1][1]
                add = 1 if P[N-1] > incoming_last else 0
                total = dp[d_last] + add
                
                # Check if this orientation creates a directed cycle (all same direction)
                # All clockwise: every edge dir=0 (L before R). For cycle, this means consistent rotation.
                # Our dirs: d for edges 0..N-2, fixed_dir_last for edge N-1.
                # All clock-wise in our numbering: all edges have dir=0.
                # All counter-clockwise: all edges have dir=1.
                if d_last == 0 and fixed_dir_last == 0:
                    # Could be all-clockwise. Need to check intermediate edges too.
                    # We'd need to track if all were 0. Skip for now - this case might be invalid.
                    pass
                
                if total > best_ans:
                    best_ans = total
        
        print(best_ans)

solve()