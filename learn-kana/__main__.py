from luts import kana_to_romaji, romaji_to_kana, simple_kana_to_romaji
import random
import os

import time

## Term info ##
term = os.popen('stty size', 'r').read().split()
term_height, term_width = int(term[0]), int(term[1]) - 5
# term_width = 30 # i have issues

gap = 3
count = 100
max_count = 50

kana_set = simple_kana_to_romaji

## Functions ##


def acceptchar(chars):
    """Convert romaji to hiragana"""

    # If this is a kana, just return it
    if ord(chars[0]) > 122:
        return chars

    # Deal with conversion
    if chars in kana_set:
        return kana_set[chars]
    else:
        return ""


def setTicker(line):
    """Sets the ticker line with data. Truncates if screen width < data len"""

    # Move to saved position
    print("\u001b[u", end="", flush=True)

    # Move up 1 line
    print("\u001b[1A", end="", flush=True)

    # Truncate the line to the terminal width
    trunc_line = "".join(line)[: int(min(term_width, max_count) / 2)][1:]
    first_char = line[0]

    # Clear line
    print(">" + " " * (term_width - 1), end="\r", flush=True)

    # Display the first char in green
    print("\u001b[37m\u001b[42;1m" + first_char, end="", flush=True)

    # Display the rest of the ticker normally
    print("\u001b[0m" + trunc_line + "\r", end="", flush=True)

    # Move down 1
    print("\u001b[1B", end="", flush=True)


def handleInput():
    """
    Accept input,
    and clean up terminal on \\n
    """
    # Clear line
    print(">" + " " * (term_width - 1), end="\r", flush=True)

    # Read from user
    data = input(">").strip()

    if len(data) == 0:
        data = " "

    # Move up 1 line
    print("\u001b[1A", end="", flush=True)

    return data


def pickKana(n):
    """Select n random kana"""
    keys = list(kana_set.keys())
    return [random.choice(keys) for _ in range(n)]

## App ##


if __name__ == "__main__":
    successes = 0

    # Pick {count} random hiragana
    challenge_set = pickKana(count)

    # newlines for ticker and input
    print("\n" * (3 + gap), end="")

    # Move up
    print(f"\u001b[{gap + 1}A", end="", flush=True)

    # Print cheat line
    print("AKS TNH MYR W\r", end="", flush=True)

    # Move up 1
    print(f"\u001b[1A", end="", flush=True)

    # Save the cursor position
    print("\u001b[s", end="", flush=True)

    start_time = time.time()
    problems = []
    completed = []

    # Run until we are out of kana
    while len(challenge_set) > 0:

        # Display the ticker
        setTicker(challenge_set)

        # read input
        data = handleInput()

        current_kana = challenge_set[0]

        if data == " ":
            continue

        # Check if we should skip
        if data == "ー":
            challenge_set = challenge_set[1:]
            completed.append((current_kana, False))
            continue

        # Check if we should stop the game
        if data == "＝":
            break

        # Check if we should explain
        if data == "＋":
            # Move to saved position
            print("\u001b[u", end="", flush=True)

            # Move down 1
            print("\u001b[1B", end="", flush=True)

            # Print the options
            print("                    \r", end="", flush=True)
            print(kana_set[current_kana], end="", flush=True)

            successes -= 1
            problems.append(current_kana)
            continue

        # Get input as hiragana
        kana = acceptchar(data)

        # Check if we should moce on
        if kana == current_kana:
            successes += 1
            completed.append((current_kana, True))
        else:
            problems.append(current_kana)
            completed.append((current_kana, False))

        challenge_set = challenge_set[1:]

    # Game end

    # Move to saved position
    print("\u001b[u", end="", flush=True)

    # Move up 1 lines
    print("\u001b[1A", end="", flush=True)

    if successes != 0:
        kps = round(round(time.time() - start_time) / successes)
    else:
        kps = 0

    # Print kana list with problems highlighted
    print(" "* max_count + "\r", end="", flush=True)
    for kana in completed:

        # Should this be Red BG?
        if not kana[1]:
            print("\u001b[37m\u001b[41;1m" + kana[0], end="", flush=True)
        else:
            print("\u001b[0m" + kana[0], end="", flush=True)

    print("\u001b[0m")

    print(
        f"Completed {successes}/{count} in ~{round(time.time() - start_time)} seconds　({kps} seconds per kana)")
    print(f"You had issues with:\n{problems}")
