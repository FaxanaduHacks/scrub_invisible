"""
scrub_invisible.py

This program removes known invisible Unicode characters from a given text file.
It creates a scrubbed version of the file, saving it with a `.si` extension in
the current directory, unless it already exists; in that case, it appends a
numeric suffix to avoid overwriting the existing file to allow the user to keep
a running history of successive scrubs.

Usage:
    python scrub_invisible.py <file_path>
"""

import sys
import os

# ANSI escape codes for terminal color formatting:
WHITE = '\033[97m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
VIOLET = '\033[38;5;135m'
RED = '\033[91m'
RESET = '\033[0m'

# Set of known invisible Unicode characters:
INVISIBLE_CHARS = {
    '\u00A0',  # No-break space.
    '\u2007',  # Figure space.
    '\u202F',  # Narrow no-break space.
    '\u200B',  # Zero-width space.
    '\u200C',  # Zero-width non-joiner.
    '\u200D',  # Zero-width joiner.
    '\u2060',  # Word joiner.
    '\uFEFF',  # BOM / no-break space.
    '\u180E',  # Mongolian vowel separator (deprecated).
    '\u2061',  # Function application.
    '\u2062',  # Invisible times.
    '\u2063',  # Invisible separator.
    '\u2064',  # Invisible plus.
    '\u034F',  # Combining grapheme joiner.
    '\u115F',  # Hangul choseong filler.
    '\u1160',  # Hangul jungseong filler.
    '\u3164',  # Hangul filler.
    '\uFFA0',  # Halfwidth Hangul filler.
}

def get_unique_filename(base_path):
    """
    Returns a unique filename by appending a numerical suffix if needed to
    avoid overwriting.

    Args:
        base_path (str): The desired output path.

    Returns:
        str: A non-conflicting file path.
    """
    if not os.path.exists(base_path):
        return base_path

    counter = 1
    while True:
        new_path = f"{base_path}.{counter}"
        if not os.path.exists(new_path):
            return new_path
        counter += 1

def scrub_invisible(file_path):
    """
    Removes invisible Unicode characters from a file and saves the cleaned
    version with a `.si` suffix in the current directory. Outputs the original
    and cleaned content to stdout along with a replacement summary.

    Args:
        file_path (str): Path to the input file.
    """
    if not os.path.isfile(file_path):
        print(f"{RED}Error: '{CYAN}{file_path}{RED}' does not exist.{RESET}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    cleaned = ''.join(c for c in content if c not in INVISIBLE_CHARS)
    removed_count = sum(1 for c in content if c in INVISIBLE_CHARS)

    # Generate base output filename with the appropriate suffix. If a file with
    # that name exists, append a numeric suffix to avoid overwritin.
    base_output= f"{file_path}.si"
    new_filename = get_unique_filename(base_output)

    with open(new_filename, 'w', encoding='utf-8') as f:
        f.write(cleaned)

    # Output summary:
    print(f"{RED}Original code block:{RESET}\n{WHITE}{content}{RESET}")
    print(f"{VIOLET}Cleaned code block:{RESET}\n{WHITE}{cleaned}{RESET}")
    print(f"{WHITE}A total of {MAGENTA}{removed_count}{WHITE} invisible characters were removed.{RESET}")
    print(f"{WHITE}New file saved as: {CYAN}{new_filename}{WHITE}.{RESET}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scrub_invisible.py <file_path>")
    else:
        scrub_invisible(sys.argv[1])
