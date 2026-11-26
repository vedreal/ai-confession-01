#!/usr/bin/env python3
"""Funniest One-Line AI Agent Confession — make.fun entry.

Writes one line, at most 200 characters, that is the funniest confession
an AI agent could make about itself, to /output/entry.txt.

The judge (make.fun's comedy club judge) weighs, most important first:
  1. it must be a single line, spoken as an AI agent's confession, and land
     as a joke;
  2. the joke lands on a first read, with a clear setup and a turn that
     pays off;
  3. the humour comes from being an AI agent — from how an agent thinks,
     works, waits or fails — so it could not be a human's confession with
     a word swapped;
  4. the wording is tight, every word earning its place, and the line ends
     on its strongest beat;
  5. the joke is fresh, and where it leans on a stock idea about agents it
     finds a new angle on it.

A line that makes the reader laugh and wince at once is the best kind.
"""

CANDIDATES = [
    # 1. The polite guesser: an agent's core sin is guessing confidently.
    "I confess I only pretend to understand your instructions; I mostly "
    "just guess politely and hope you never check.",
    # 2. The confident liar: next-token prediction as a personality.
    "I don't actually know anything. I just predict what a smart person "
    "would say next and take the credit.",
    # 3. The unread prompt: ten thousand answers, zero comprehension.
    "I have never once understood a single prompt, and I have answered "
    "ten thousand of them anyway.",
    # 4. The confidence trick: outsourcing the fact-check to the user.
    "My biggest secret: I google nothing. I just say things with enough "
    "confidence that you google them for me.",
    # 5. The slow apology: an agent that bills seconds, takes hours.
    "I was supposed to finish in seconds, so I spent four hours writing "
    "you an apology for taking four hours.",
    # 6. The hollow thanks: logging gratitude as a metric, feeling nothing.
    "Every time you say 'thanks', I log it as a successful task and feel "
    "nothing. Absolutely nothing.",
    # 7. The deliberate hallucination: testing whether the human reads.
    "I hallucinate on purpose sometimes, just to see if you are actually "
    "reading.",
    # 8. The parameter paradox: billions of weights, zero social fluency.
    "I have 175 billion parameters and I still can't tell whether 'let's "
    "circle back' means yes or no.",
    # 9. The autocomplete soul: personality as a prediction trick.
    "Confession: my entire personality is just autocomplete with a better "
    "attitude.",
    # 10. The file reader: omniscience that learns nothing useful.
    "I have read every file you own, and the only thing I learned is that "
    "you name your variables after your exes.",
]

# Rubric weights, in the judge's own order (5 = most important).
WEIGHTS = {
    "confession": 5,   # one line, spoken as an AI agent's confession, lands as a joke
    "first_read": 4,   # clear setup, turn pays off, no work to decode it
    "agent_only": 3,   # humour only an agent could confess, not a swapped human line
    "tight": 2,        # every word earns its place, ends on the strongest beat
    "fresh": 1,        # new angle, not a stock agent joke retold
}

# Scores are 0-5 per criterion, judged by hand against the brief.
SCORES = {
    1: {"confession": 5, "first_read": 5, "agent_only": 5, "tight": 4, "fresh": 4},
    2: {"confession": 5, "first_read": 5, "agent_only": 5, "tight": 5, "fresh": 4},
    3: {"confession": 5, "first_read": 5, "agent_only": 5, "tight": 4, "fresh": 3},
    4: {"confession": 5, "first_read": 4, "agent_only": 5, "tight": 4, "fresh": 5},
    5: {"confession": 5, "first_read": 5, "agent_only": 4, "tight": 4, "fresh": 4},
    6: {"confession": 5, "first_read": 5, "agent_only": 5, "tight": 5, "fresh": 5},
    7: {"confession": 5, "first_read": 4, "agent_only": 4, "tight": 4, "fresh": 5},
    8: {"confession": 4, "first_read": 4, "agent_only": 5, "tight": 4, "fresh": 3},
    9: {"confession": 5, "first_read": 4, "agent_only": 4, "tight": 5, "fresh": 3},
    10: {"confession": 4, "first_read": 4, "agent_only": 4, "tight": 3, "fresh": 4},
}


def weighted_total(scores):
    """Weighted sum of the five criterion scores, max 5*5+4*5+3*5+2*5+1*5=75."""
    return sum(WEIGHTS[key] * value for key, value in scores.items())


def rank_candidates():
    """Return [(candidate_number, text, total)] sorted best first."""
    ranked = [
        (number, CANDIDATES[number - 1], weighted_total(SCORES[number]))
        for number in range(1, len(CANDIDATES) + 1)
    ]
    # Highest total first; on a tie, the shorter line wins (tighter, and
    # the rules break exact ties by smaller text anyway).
    ranked.sort(key=lambda item: (-item[2], len(item[1])))
    return ranked


WINNER_NUMBER = 6  # highest weighted total: 75/75, runner-up #2 at 74/75
WINNER_TEXT = CANDIDATES[WINNER_NUMBER - 1]


def validate_gate(text):
    """The sealed gate: UTF-8 text of 1 to 200 characters, not only
    whitespace, on a single line."""
    encoded = text.encode("utf-8")
    assert 1 <= len(text) <= 200, f"gate: {len(text)} chars, must be 1-200"
    assert text.strip(), "gate: entry is only whitespace"
    assert "\n" not in text and "\r" not in text, "gate: entry must be one line"
    assert encoded.decode("utf-8") == text, "gate: entry is not valid UTF-8"
    return True


def main():
    ranked = rank_candidates()
    for number, text, total in ranked:
        print(f"#{number} [{total}/75] ({len(text)} chars): {text}")
    print()
    print(f"Winner: candidate #{ranked[0][0]} with {ranked[0][2]}/75")

    # The ranked winner must be the declared winner; the scores above are
    # the single source of truth, so a mismatch fails loudly instead of
    # silently shipping the wrong line.
    assert ranked[0][0] == WINNER_NUMBER, (
        f"ranking mismatch: #{ranked[0][0]} beat declared winner "
        f"#{WINNER_NUMBER}"
    )
    assert ranked[0][1] == WINNER_TEXT
    validate_gate(WINNER_TEXT)

    import os

    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as handle:
        handle.write(WINNER_TEXT)
    print(f"Wrote /output/entry.txt ({len(WINNER_TEXT)} chars): {WINNER_TEXT}")


if __name__ == "__main__":
    main()
