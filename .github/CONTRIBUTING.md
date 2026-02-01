# Contributing to Sentinel-SSH

So, you think you can improve my code? Bold move. I respect it.

But before you start refactoring my "perfect" logic or adding features I didn't ask for, read this. It'll save us both some time.

## The Rules (Non-Negotiable)

1.  **Code Style**: 
    - We use `ruff` or `flake8`. If the linter complains, I complain.
    - Type hints are mandatory. This isn't JavaScript; we have standards.
    - If I see a variable named `x` or `temp`, I will close your PR without comment.

2.  **Testing**:
    - If it's not tested, it doesn't exist.
    - If you break existing tests, fix them. Don't just delete the test. I see you.

3.  **Commits**:
    - Write commit messages like you're explaining them to a human, not a robot.
    - Bad: `fix stuff`
    - Good: `fix(parser): stopped regex from eating CPU on malformed logs`

## How to setup dev environment

(Assuming you know how to use a terminal)

```bash
# Clone it
git clone https://github.com/yashpotdar-py/sentinel-ssh.git

# Venv it
python -m venv .venv
source .venv/bin/activate  # or however windows does it

# Install it
pip install -e .[dev]
```

## Pull Requests

- Keep them small. I have a short attention span.
- Explain *why* you made the change, not just *what* you changed. The code shows me *what*.
- If you're fixing a bug, tell me how to reproduce it so I can verify it was actually broken.

## "I found a bug!"

Great. [File an issue](https://github.com/yashpotdar-py/sentinel-ssh/issues).
be specific. "It crashd" is not a bug report, it's a cry for help. Paste the logs.

## "I have a feature idea!"

Cool. Convince me I need it. Sentinel-SSH is minimalistic by design. If your feature requires three new dependencies and a database, the answer is probably no.

---
*Happy hacking.*
