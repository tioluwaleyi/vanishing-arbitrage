# Vanishing Arbitrage

This repository contains the reference solution, brute-force verifier, randomized test generator, official test cases, and Qwen attempts for the Vanishing Arbitrage problem.

## Requirements

- Python 3.11+
- No third-party Python packages are required.

## Run the Reference Solution

From the project root:

```bash
python solution.py < test_cases/1.in
```

On Windows PowerShell:

```powershell
Get-Content .\test_cases\1.in -Raw | python .\solution.py
```

The output can be compared with:

```text
test_cases/1.out
```

## Run the Brute-Force Solution

`solution_bf.py` is an independent brute-force implementation intended only for small instances.

```bash
python solution_bf.py < test_cases/1.in
```

Do not use it for large inputs because it enumerates subsets and execution orders.

## Run Randomized Verification

`generator.py` generates small random instances and compares the optimized solution against the brute-force oracle.

Run:

```bash
python generator.py
```

A successful run ends with:

```text
ALL RANDOMIZED TESTS PASSED
```

## Run All Official Tests

### PowerShell

```powershell
1..7 | ForEach-Object {
    $actual = (
        Get-Content ".\test_cases\$_.in" -Raw |
        python .\solution.py
    ).Trim()

    $expected = Get-Content ".\test_cases\$_.out" -Raw

    if ($null -eq $expected) {
        Write-Host "Test $_ FAIL - output file is empty"
    }
    elseif ($actual -eq $expected.Trim()) {
        Write-Host "Test $_ PASS"
    }
    else {
        Write-Host "Test $_ FAIL - expected $($expected.Trim()), got $actual"
    }
}
```

Expected result:

```text
Test 1 PASS
Test 2 PASS
Test 3 PASS
Test 4 PASS
Test 5 PASS
Test 6 PASS
Test 7 PASS
```

## Files

- `problem.md` — problem statement.
- `idea.md` — development process, rejected ideas, and final approach.
- `solution.md` — algorithm explanation and correctness proof.
- `solution.py` — optimized reference solution.
- `solution_bf.py` — brute-force correctness oracle for small inputs.
- `generator.py` — randomized differential testing script.
- `requirements.json` — time and memory limits.
- `test_cases/` — official input/output tests.
- `qwen/` — three independent Qwen attempts and conversation links.

## Complexity

The reference solution runs in:

- **Time:** `O(N)`
- **Auxiliary DP space:** `O(1)`
- **Total memory:** `O(N)` for the input arrays.