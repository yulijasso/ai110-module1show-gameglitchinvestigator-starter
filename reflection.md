# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start
  (for example: "the secret number kept changing" or "the hints were backwards").

When I first ran the game, it looked like a normal number guessing app on the surface, but nothing actually worked the way it should. The hints were completely backwards — if my guess was too high, it told me to go higher, which just sent me further from the answer every time. I also noticed the secret number would randomly change type between an integer and a string on certain attempts, which messed up the comparisons entirely. On top of that, after winning or losing, clicking "New Game" didn't actually reset things, so I was stuck on the game-over screen until I refreshed the whole page.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used Claude for this entire project. **Correct suggestion:** I asked the AI to explain the scoring bug in `update_score()`, and it correctly identified that on even-numbered attempts, a "Too High" wrong guess was rewarding the player +5 points instead of penalizing them. It suggested removing the `attempt_number % 2 == 0` branch so wrong guesses always deduct points. I verified this by writing a pytest case (`test_too_high_always_penalizes`) that checks both even and odd attempts return a score of 95 from a starting score of 100 — the test passed after the fix. **Incorrect/misleading suggestion:** When I first asked the AI about the `check_guess()` function, it focused on the reversed hint messages but didn't immediately flag the `TypeError` fallback block that was casting guesses to strings for comparison. That block was actually the deeper problem — it meant `"9" > "100"` evaluated to `True` because Python compares strings character by character, not numerically. I caught this myself by looking at the Developer Debug Info panel and noticing the type of the secret changing, then asked the AI to explain why string comparison would break things, which it did well once I pointed it in the right direction.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I used a combination of manual testing in the live Streamlit app and automated pytest cases. For manual testing, I opened the Developer Debug Info panel to see the secret number, then made deliberate guesses — for instance, guessing 60 when the secret was 50 to confirm the hint now correctly says "Go LOWER!" instead of the old reversed "Go HIGHER!" message. For automated testing, I ran `pytest tests/test_game_logic.py` after refactoring the logic into `logic_utils.py`. I wrote targeted tests for each bug fix: `test_high_guess_says_go_lower` and `test_low_guess_says_go_higher` verified the hint messages, while `test_too_high_always_penalizes` confirmed that "Too High" deducts 5 points on both even and odd attempts. All 7 tests passed, which gave me confidence the fixes were solid. The AI helped by generating the initial test structure and suggesting what assertions to use — for example, it recommended checking that the message string contains "LOWER" rather than matching the full emoji string, which made the tests less brittle.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

The secret number kept changing because every time you interact with a Streamlit app — clicking a button, typing in a box — the entire script reruns from top to bottom. So if you just set `secret = random.randint(1, 100)` without protecting it, you get a brand new random number on every single click. The way I'd explain it to a friend is: imagine a web page that reloads itself every time you do anything, and all your variables get wiped clean each reload. `session_state` is like a sticky note that survives those reloads — you write your data there, and it stays put. The fix was wrapping the secret number in an `if "secret" not in st.session_state` check, so it only generates a new number the very first time and keeps it the same for the rest of the game.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit I want to keep is always checking the actual app behavior against what the code says it should do, not just trusting that the logic "looks right." The Developer Debug panel was a lifesaver here, and I want to build that kind of visibility into future projects — whether it's debug logs, print statements, or a test suite. Next time I work with AI on code, I'd be more upfront about asking it to explain its reasoning rather than just accepting the first fix it suggests, since some of its initial answers were surface-level and missed deeper issues. This project really drove home that AI-generated code can look clean and professional while still being completely wrong — it taught me to treat AI output as a first draft that needs hands-on verification, not a finished product.
