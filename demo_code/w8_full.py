# PART 1: HOW TO MATCH WHICH ALGO IS BEST FROM THE QUESTION SIGNALS
# 1. GREEDY
#    - Prompt Signals: "Min/max value", local best choice is always globally optimal
#      (e.g., standard US coins {1, 5, 10, 25}, interval scheduling).
#    - Trap: Fails when choices affect future availability/fit (non-canonical coins
#      like {1, 3, 4} for target 6: Greedy picks 4+1+1 (3 coins) instead of 3+3 (2 coins)).
#
# 2. DYNAMIC PROGRAMMING (DP)
#    - Prompt Signals: "Find minimum/maximum count/cost", "Count total ways",
#      "Is it possible to reach...".
#    - Core Properties:
#      a) Optimal Substructure: Optimal solution to target X built from optimal
#         solutions of smaller targets (X - coin).
#      b) Overlapping Subproblems: Same remainder computed repeatedly across branches.
#    - Why NOT Backtracking here: We only need one aggregate value (min count), not
#      every explicit path. Caching sub-states reduces O(N^A) to O(A * N).
#
# 3. BACKTRACKING
#    - Prompt Signals: "Find ALL possible...", "Return EVERY combination...",
#      "Generate all valid subsets/permutations...".
#    - Core Properties: Must build and output every valid configuration.
#      Uses DFS over decision tree: Choose -> Explore -> Un-choose (undo), plus Pruning.
#    - Small Change to Make Coin Change a Backtracking Problem:
#      Change goal from "Find minimum number of coins for 6¢"
#      to "Find ALL unique combinations of coins that sum to 6¢".

# ==============================================================================
# PART 2: GENERIC LINE-BY-LINE PLANS FOR EACH ALGORITHM
# ==============================================================================
# --- GREEDY LINE-BY-LINE PLAN ---
# 1. Sort `choices` by local optimality metric.
# 2. Initialize `state` and `result`.
# 3. Loop through each `candidate` in `choices`:
# 4.   While `candidate` is valid for `state`:
# 5.     Commit `candidate` to `result`.
# 6.     Advance `state` using `candidate`.
# 7. Return `result` if target `state` reached, else fallback.
#
# --- DYNAMIC PROGRAMMING (TOP-DOWN MEMOIZATION) LINE-BY-LINE PLAN ---
# 1. Initialize `memo` cache with base cases.
# 2. Define recursive helper `dp(state)`:
# 3.   If `state` in `memo`, return `memo[state]`.
# 4.   If `state` is invalid, return base identity.
# 5.   Initialize `best` for current `state`.
# 6.   Loop through each `choice` in `choices`:
# 7.     Update `best = combine(best, cost + dp(next_state))`.
# 8.   Store `memo[state] = best` and return `best`.
# 9. Invoke `dp(target_state)` and return result.
#
# --- DYNAMIC PROGRAMMING (BOTTOM-UP TABULATION) LINE-BY-LINE PLAN ---
# 1. Initialize `dp` table sized for all states with default values.
# 2. Set base cases in `dp` table.
# 3. Loop `state` from smallest subproblem up to `target_state`:
# 4.   Loop through each `choice` in `choices`:
# 5.     If `prev_state` is valid:
# 6.       Update `dp[state] = combine(dp[state], cost + dp[prev_state])`.
# 7. Return `dp[target_state]` if reachable, else fallback.
#
# --- BACKTRACKING LINE-BY-LINE PLAN ---
# 1. Initialize `results` list.
# 2. Define helper `backtrack(path, state, choices)`:
# 3.   If `is_complete(path, state)`, append `path.copy()` to `results` and return.
# 4.   If `is_invalid(state)`, return.
# 5.   Loop through each `choice` in `choices`:
# 6.     Append `choice` to `path`.
# 7.     Call `backtrack(path, next_state, next_choices)`.
# 8.     Pop `choice` from `path`.
# 9. Invoke `backtrack([], initial_state, choices)` and return `results`.

# ==============================================================================
    # PART 2: LINE-BY-LINE PLANS FOR EACH ALGORITHM
    # ==============================================================================
    # --- GREEDY LINE-BY-LINE PLAN ---
    # 1. Sort coins in descending order (largest to smallest).
    # 2. Initialize coin counter `count = 0`.
    # 3. Loop through each `coin` in sorted `coins`:
    # 4.   While remaining `amount >= coin`:
    # 5.     Subtract `coin` from `amount`.
    # 6.     Increment `count` by 1.
    # 7. Return `count` if `amount == 0`, else `-1` (if target cannot be formed).
    #
    # --- DYNAMIC PROGRAMMING (BOTTOM-UP) LINE-BY-LINE PLAN ---
    # 1. Create array `dp` of size `amount + 1`, filled with `float('inf')`.
    # 2. Set base case `dp[0] = 0` (0 coins needed to make 0¢).
    # 3. Loop sub-amount `a` from `1` up to `amount`:
    # 4.   Loop through each `c` in `coins`:
    # 5.     If `a - c >= 0` (coin fits into current sub-amount):
    # 6.       Update `dp[a] = min(dp[a], 1 + dp[a - c])`.
    # 7. Return `dp[amount]` if not `float('inf')`, else `-1`.
    #
    # --- BACKTRACKING (ALL COMBINATIONS) LINE-BY-LINE PLAN ---
    # 1. Initialize `results = []` to store all valid coin combinations.
    # 2. Define helper `backtrack(path, start, rem)`:
    # 3.   Base Case (Complete): If `rem == 0`, append `path.copy()` to `results` and return.
    # 4.   Prune Case: If `rem < 0`, return immediately (sum exceeded target).
    # 5.   Loop index `i` from `start` to `len(coins) - 1` (never look backward -> Combinations):
    # 6.     CHOOSE: Append `coins[i]` to `path`.
    # 7.     EXPLORE: Call `backtrack(path, i, rem - coins[i])` (pass `i` to allow reusing coin).
    # 8.     UN-CHOOSE: Pop last coin from `path` to restore state for next branch.
    # 9. Invoke `backtrack([], 0, amount)` and return `results`.

# ==============================================================================
# PART 3: UMPIRE WORKFLOW & IMPLEMENTATIONS
# ==============================================================================
# Understand:
#   - Input: coins = [1, 3, 4], amount = 6
#   - Output (Greedy/DP): int (min coins, or -1 if impossible)
#   - Output (Backtracking variant): list[list[int]] (all unique coin combinations)
#   - Edge cases: amount = 0 -> 0 coins (or [[]] for combinations); unreachable -> -1 (or [])


# ------------------------------------------------------------------------------
# 1. GREEDY SOLUTION (Fails on {1, 3, 4} for 6¢)
# ------------------------------------------------------------------------------

# From Greedy to DP: 5¢ with {1, 3, 4}
# The Goal: Find the absolute minimum number of coins.
# Greedy Logic: Take the biggest coin first, no matter what.
# DP Logic: Try every coin as a first step and see which one leads to the best future.

# 1. Sort coins in descending order (largest to smallest).
# 2. Initialize coin counter `count = 0`.
# 3. Loop through each `coin` in sorted `coins`:
# 4.   While remaining `amount >= coin`:
# 5.     Subtract `coin` from `amount`.
# 6.     Increment `count` by 1.
# 7. Return `count` if `amount == 0`, else `-1` (if target cannot be formed).

def coin_change_greedy(coins: list[int], amount: int) -> int:
    # Sort descending to always grab largest coin first
    sorted_coins = sorted(coins, reverse=True)
    count = 0

    for coin in sorted_coins:
        while amount >= coin:
            amount -= coin
            count += 1

    return count if amount == 0 else -1


# ------------------------------------------------------------------------------
# 2. STEP-BY-STEP REFACTOR: GREEDY -> DYNAMIC PROGRAMMING
# ------------------------------------------------------------------------------

# Refactor Step 2A: Naive Recursion (Try every coin as first step, no caching)
# Time: O(N^A) exponential | Space: O(A) recursion stack
def coin_change_recursive(coins: list[int], amount: int) -> int:
    def dfs(rem: int) -> float:
        if rem == 0:
            return 0
        if rem < 0:
            return float('inf')

        min_coins = float('inf')
        for c in coins:
            # Try coin `c` and see what best future it leads to
            min_coins = min(min_coins, 1 + dfs(rem - c))
        return min_coins

    res = dfs(amount)
    return int(res) if res != float('inf') else -1


# Refactor Step 2B: Top-Down DP with Memoization (Cache overlapping subproblems)
# Time: O(A * N) | Space: O(A) memo + recursion stack
def coin_change_memo(coins: list[int], amount: int) -> int:
    memo: dict[int, float] = {0: 0}

    def dfs(rem: int) -> float:
        if rem in memo:
            return memo[rem]
        if rem < 0:
            return float('inf')

        min_coins = float('inf')
        for c in coins:
            min_coins = min(min_coins, 1 + dfs(rem - c))

        memo[rem] = min_coins
        return min_coins

    res = dfs(amount)
    return int(res) if res != float('inf') else -1


# Refactor Step 2C: Bottom-Up DP with Tabulation (Iterative array, no recursion overhead)
# Time: O(A * N) | Space: O(A) dp array
# --- DYNAMIC PROGRAMMING (BOTTOM-UP) LINE-BY-LINE PLAN ---
# 1. Create array `counts` of size `amount + 1`, filled with `float('inf')`.
# 2. Set base case `counts[0] = 0` (0 coins needed to make 0¢).
# 3. Loop `sub_amount` from `1` up to `amount`:
# 4.   Loop through each `coin` in `coins`:
# 5.     If `sub_amount >= coin` (mirrors `amount >= coin` from greedy):
# 6.       Update `counts[sub_amount] = min(counts[sub_amount], 1 + counts[sub_amount - coin])`.
# 7. Return `counts[amount]` if not `float('inf')`, else `-1`.



# 2. Refactored to Bottom-Up DP (`count` -> `counts` array, `amount >= coin` -> `sub_amount >= coin`)
def coin_change_dp(coins: list[int], amount: int) -> int:
    counts = [float('inf')] * (amount + 1)
    counts[0] = 0

    for sub_amount in range(1, amount + 1):
        for coin in coins:
            if sub_amount >= coin:
                counts[sub_amount] = min(counts[sub_amount], 1 + counts[sub_amount - coin])

    count = counts[amount]
    return int(count) if count != float('inf') else -1


# ------------------------------------------------------------------------------
# 3. BACKTRACKING SOLUTION (Modified Problem: Find ALL Unique Combinations for 6¢)
# ------------------------------------------------------------------------------
# Why standard Coin Change is NOT a Backtracking problem:
#   Standard Coin Change asks for a single minimum count. Exploring all paths without
#   memoization re-computes the same remainders exponentially.
#
# Small change to make it Backtracking:
#   Ask for "ALL unique combinations of coins that sum to 6¢".
#   Shape: Combinations (order doesn't matter, pass `start` index so we never look back).
#   Time: Exponential O(N^(A/min_coin)) | Space: O(A/min_coin) path + recursion depth
def all_coin_combinations_backtrack(coins: list[int], amount: int) -> list[list[int]]:
    results: list[list[int]] = []

    def backtrack(path: list[int], start: int, rem: int) -> None:
        # 1. Complete Check: exact target reached
        if rem == 0:
            results.append(path.copy())
            return

        # 2. Prune Check: sum exceeded target, abandon branch immediately
        if rem < 0:
            return

        # 3. Explore Choices: start at `start` index to avoid duplicate permutations
        for i in range(start, len(coins)):
            path.append(coins[i])                  # Choose
            backtrack(path, i, rem - coins[i])     # Explore (reuse coin `i` allowed)
            path.pop()                             # Un-choose (Backtrack)

    backtrack([], 0, amount)
    return results


# ==============================================================================
# PART 4: DEMO DRIVER & TRACE VERIFICATION
# ==============================================================================
if __name__ == "__main__":
    demo_coins = [1, 3, 4]
    demo_amount = 6

    print(f"--- Coin Change Instructor Demo: {demo_amount}¢ with {demo_coins} ---")
    print(f"1. Greedy Result (4+1+1):        {coin_change_greedy(demo_coins, demo_amount)} coins (Suboptimal!)")
    print(f"2A. Naive Recursive Result:      {coin_change_recursive(demo_coins, demo_amount)} coins")
    print(f"2B. Top-Down Memo DP Result:     {coin_change_memo(demo_coins, demo_amount)} coins")
    print(f"2C. Bottom-Up Tabulation Result: {coin_change_dp(demo_coins, demo_amount)} coins (Optimal: 3+3)")
    print(f"3. Backtracking All Combos:      {all_coin_combinations_backtrack(demo_coins, demo_amount)}")
# ==============================================================================
# PART 2: GENERIC LINE-BY-LINE PLANS FOR EACH ALGORITHM
# ==============================================================================
# --- GREEDY LINE-BY-LINE PLAN ---
# 1. Sort `choices` by local optimality metric.
# 2. Initialize `state` and `result`.
# 3. Loop through each `candidate` in `choices`:
# 4.   While `candidate` is valid for `state`:
# 5.     Commit `candidate` to `result`.
# 6.     Advance `state` using `candidate`.
# 7. Return `result` if target `state` reached, else fallback.
#
# --- DYNAMIC PROGRAMMING (TOP-DOWN MEMOIZATION) LINE-BY-LINE PLAN ---
# 1. Initialize `memo` cache with base cases.
# 2. Define recursive helper `dp(state)`:
# 3.   If `state` in `memo`, return `memo[state]`.
# 4.   If `state` is invalid, return base identity.
# 5.   Initialize `best` for current `state`.
# 6.   Loop through each `choice` in `choices`:
# 7.     Update `best = combine(best, cost + dp(next_state))`.
# 8.   Store `memo[state] = best` and return `best`.
# 9. Invoke `dp(target_state)` and return result.
#
# --- DYNAMIC PROGRAMMING (BOTTOM-UP TABULATION) LINE-BY-LINE PLAN ---
# 1. Initialize `dp` table sized for all states with default values.
# 2. Set base cases in `dp` table.
# 3. Loop `state` from smallest subproblem up to `target_state`:
# 4.   Loop through each `choice` in `choices`:
# 5.     If `prev_state` is valid:
# 6.       Update `dp[state] = combine(dp[state], cost + dp[prev_state])`.
# 7. Return `dp[target_state]` if reachable, else fallback.
#
# --- BACKTRACKING LINE-BY-LINE PLAN ---
# 1. Initialize `results` list.
# 2. Define helper `backtrack(path, state, choices)`:
# 3.   If `is_complete(path, state)`, append `path.copy()` to `results` and return.
# 4.   If `is_invalid(state)`, return.
# 5.   Loop through each `choice` in `choices`:
# 6.     Append `choice` to `path`.
# 7.     Call `backtrack(path, next_state, next_choices)`.
# 8.     Pop `choice` from `path`.
# 9. Invoke `backtrack([], initial_state, choices)` and return `results`.