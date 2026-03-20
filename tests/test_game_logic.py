from logic_utils import check_guess, update_score

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"

# --- Tests targeting Bug Fix 1: no more string comparison fallback ---

def test_high_guess_says_go_lower():
    # Bug fix: hints should not be reversed
    outcome, message = check_guess(60, 50)
    assert "LOWER" in message

def test_low_guess_says_go_higher():
    # Bug fix: hints should not be reversed
    outcome, message = check_guess(40, 50)
    assert "HIGHER" in message

# --- Tests targeting Bug Fix 2: consistent scoring on wrong guesses ---

def test_too_high_always_penalizes():
    # Bug fix: "Too High" should deduct 5 points on EVERY attempt, not reward on even ones
    score_after_even = update_score(100, "Too High", attempt_number=2)
    score_after_odd = update_score(100, "Too High", attempt_number=3)
    assert score_after_even == 95
    assert score_after_odd == 95

def test_too_low_penalizes():
    score = update_score(100, "Too Low", attempt_number=1)
    assert score == 95
