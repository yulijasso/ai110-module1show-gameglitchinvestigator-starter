# Bugs Found in Glitchy Guesser

## Bug 1 — Reversed hints (Fixed)
**File:** `app.py` — `check_guess()` function
**Problem:** The hints were backwards. When the guess was too high, the message said "Go HIGHER!" and when too low it said "Go LOWER!"
**Fix:** Swapped the messages so "Go LOWER!" appears when guess > secret, and "Go HIGHER!" when guess < secret.

## Bug 2 — Secret type randomly switches (Fixed)
**File:** `app.py` — submit logic
**Problem:** On even-numbered attempts, the secret number is converted to a string before comparison. This causes incorrect results because string comparison is lexicographic (e.g. `"9" > "100"` evaluates to `True`).
**Fix:** Remove the type-switching logic and always compare against the integer secret.

## Bug 3 — New Game does not reset status (Fixed)
**File:** `app.py` — new game button handler
**Problem:** Clicking "New Game" after winning or losing did not reset `st.session_state.status` to `"playing"`, so the game was immediately blocked by the status check and `st.stop()` was called every run.
**Fix:** Added `st.session_state.status = "playing"` to the new game handler.
