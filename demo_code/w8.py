# From Greedy to DP: 5¢ with {1, 3, 4}
# The Goal: Find the absolute minimum number of coins.
# Greedy Logic: Take the biggest coin first, no matter what.
# DP Logic: Try every coin as a first step and see which one leads to the best future.

#  Sort `choices` by local optimality metric.
#  Initialize `state` and `result`.
#   Loop through each `candidate` in `choices`:
#     While `candidate` is valid for `state`:
#       Commit `candidate` to `result`.
#       Advance `state` using `candidate`.
#   Return `result` if target `state` reached, else fallback.



def coin_change_greedy(coins: list[int], amount: int) -> int:

    sorted_coins = sorted(coins, reverse=True)
    count = 0

    for coin in sorted_coins:
        while amount >= coin:
            amount -= coin
            count += 1

    return count if amount == 0 else -1







assert coin_change_greedy([1, 3, 4], 5) == 2, "Greedy works for 5 cents (4 + 1 = 2 coins)"
assert coin_change_greedy([1, 3, 4], 6) == -1, "Greedy fails for 6 cents with coins [1, 3, 4]"




# --- DYNAMIC PROGRAMMING (BOTTOM-UP TABULATION) ---
# Initialize `dp` table sized for all states with default values.
# Set base cases in `dp` table.
    # Loop `state` from smallest subproblem up to `target_state`:
    #   Loop through each `choice` in `choices`:
    #     If `prev_state` is valid:
    #       Update `dp[state] = combine(dp[state], cost + dp[prev_state])`.
    # Return `dp[target_state]` if reachable, else fallback.


def coin_change_dp(coins: list[int], amount: int) -> int:
    counts = [float('inf')] * (amount + 1)
    counts[0] = 0

    for sub_amount in range(1, amount + 1):
        for coin in coins:
            if sub_amount >= coin:
                counts[sub_amount] = min(counts[sub_amount], 1 + counts[sub_amount - coin])

    count = counts[amount]
    return int(count) if count != float('inf') else -1
























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