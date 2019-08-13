from luts import kana_to_romaji, romaji_to_kana, simple_kana_to_romaji
import random
import os

## Term info ##
term = os.popen('stty size', 'r').read().split()
term_height, term_width = int(term[0]), int(term[1]) - 5
# term_width = 30 # i have issues

gap = 5

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
    trunc_line = "".join(line)[: int(term_width / 2)][1:]
    first_char = line[0]

    # Clear line
    print(">" + " " * (term_width - 1), end="\r", flush=True)

    # Display the first char in green
    print("\u001b[37m\u001b[42;1m" + first_char, end="", flush=True)

    # Display the rest of the ticker normally
    print("\u001b[0m" + trunc_line, flush=True)


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

    # Pick 100 random hiragana
    challenge_set = pickKana(20)

    # newlines for ticker and input
    print("\n" * (2 + gap), end="")

    # Move up 
    print(f"\u001b[{gap}A", end="", flush=True)

    # Save the cursor position
    print("\u001b[s", end="", flush=True)

    # Run until we are out of kana
    while len(challenge_set) > 0:

        # Display the ticker
        setTicker(challenge_set)

        # read input
        data = handleInput()

        # Check if we should skip
        if data == "ー":
            challenge_set = challenge_set[1:]
            continue
        
        # Check if we should stop the game
        if data == "＝":
            break

        # Get input as hiragana
        kana = acceptchar(data)

        # Check if we should moce on
        if kana == challenge_set[0]:
            challenge_set = challenge_set[1:]
