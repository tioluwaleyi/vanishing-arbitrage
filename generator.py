import random
import subprocess
import sys


PYTHON = sys.executable
FAST = "solution.py"
BRUTE = "solution_bf.py"


def generate_case(rng, max_n=7):
    n = rng.randint(1, max_n)

    # Cycles require at least 3 vertices.
    if n < 3:
        t = 0
    else:
        t = rng.randint(0, 1)

    # Include negative, zero and positive profits.
    p = [rng.randint(-3, 8) for _ in range(n)]

    edge_count = n if t == 1 else n - 1

    edges = []
    for _ in range(edge_count):
        a = rng.randint(0, 8)
        b = rng.randint(0, 8)
        edges.append((a, b))

    return n, t, p, edges


def format_case(n, t, p, edges):
    lines = [
        f"{n} {t}",
        " ".join(map(str, p)),
    ]

    for a, b in edges:
        lines.append(f"{a} {b}")

    return "\n".join(lines) + "\n"


def run_program(filename, case):
    result = subprocess.run(
        [PYTHON, filename],
        input=case,
        text=True,
        capture_output=True,
        timeout=10,
    )

    if result.returncode != 0:
        print(f"\n{filename} crashed:")
        print(result.stderr)
        sys.exit(1)

    return result.stdout.strip()


def main():
    seed = 20261003
    tests = 1000

    rng = random.Random(seed)

    print(f"Seed: {seed}")
    print(f"Running {tests} randomized comparisons...")

    for test_id in range(1, tests + 1):
        n, t, p, edges = generate_case(rng)
        case = format_case(n, t, p, edges)

        brute = run_program(BRUTE, case)
        fast = run_program(FAST, case)

        if brute != fast:
            print("\nMISMATCH FOUND")
            print("=" * 50)
            print(f"Test: {test_id}")
            print("\nInput:")
            print(case, end="")
            print(f"\nBrute-force output: {brute}")
            print(f"Optimized output:   {fast}")
            print("=" * 50)
            return

        if test_id % 100 == 0:
            print(f"{test_id}/{tests} passed")

    print("\nALL RANDOMIZED TESTS PASSED")


if __name__ == "__main__":
    main()