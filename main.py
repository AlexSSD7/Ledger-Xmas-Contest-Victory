import numpy
from btclib import bip39
from threading import Thread
import itertools
import json
import re
import time
import datetime
import ago
from si_prefix import si_format
from stuff import hints, mnemonics


def prettify_time(secs):
    # Converts bare seconds to human-readable format (like 3 hours 28 minutes)
    if secs <= 60:
        # We don't need to display milliseconds, if we have seconds
        precision = 1
    else:
        precision = 2
    time_future = datetime.datetime.now() + datetime.timedelta(seconds=secs)
    prettified_time = ago.human(time_future, future_tense="{}", precision=precision)
    return prettified_time


# Reading BIP-39 dictionary
with open("dictdata/english.txt", "r") as f:
    mnemonics_all = f.read().split("\n")[:-1]

# Checking if given words are valid
for word in mnemonics:
    if word not in mnemonics_all:
        print("NOT VALID MNEMONICS")
        exit()

# Check hints
# print(hints)

possible_mnemonics = mnemonics.copy()

# Checking amount of words that seems like to be ok with given hint
hint_chars = {}
unknown_hints = 0
for hint_char in hints:
    if hint_char != "" and len(hint_char) == 1:
        if hint_char not in hint_chars:
            hint_chars[hint_char] = 0
        hint_chars[hint_char] += 1
    elif hint_char == "":
        unknown_hints += 1


# Checking amount of words starting with N letter
word_chars = {}
for word in mnemonics:
    word_char = word[0]
    if word_char not in word_chars:
        word_chars[word_char] = 0
    word_chars[word_char] += 1


# Checking hints
for char, count in word_chars.items():
    hint_char_count = hint_chars[char]
    if count != hint_char_count:
        raise(Exception("Mnemonics aren't matched with hints"))


# Get mnemonics available for part with no hint (unused with second hint)
mnemonics_if_null = mnemonics.copy()
for word in mnemonics:
    f_letter = word[0]
    if f_letter in hint_chars:
        word_match_count = 0
        for word_temp in mnemonics:
            if re.match(r"^" + f_letter, word_temp):
                word_match_count += 1
        if hint_chars[f_letter] == word_match_count:
            mnemonics_if_null.remove(word)

# Constructing list with possible values
all_possible_combinations = []
for char in hints:
    if len(char) == 1:
        combos = []
        for word in mnemonics:
            if word[0] == char:
                combos.append(word)
        all_possible_combinations.append(combos)
    elif char == "":
        all_possible_combinations.append(mnemonics_if_null)

# Writing it to file (extra checkpoint)
# with open("payload.out.txt", "w") as f:
#     f.write(json.dumps(all_possible_combinations))

num_possible_combos = [len(x) for x in all_possible_combinations]

hint_characters_order = [x[0][0] for x in all_possible_combinations]
available_char_count = {x[0][0]: len(x) for x in all_possible_combinations}
# Calculating possible filtered (with no repetitions) combination count
total_possible_combos = []
for char in hint_characters_order:
    total_possible_combos.append(available_char_count[char])
    available_char_count[char] -= 1

# Producing filtered combo count
total_possible_combos = numpy.prod(total_possible_combos)

# Producing unfiltered combo count
unfiltered_possible_combos = numpy.prod(num_possible_combos)

# Displaying all stuff
print("Total combos (with repetitions)   : {0}".format(unfiltered_possible_combos))
print("Total combos (without repetitions): {0}".format(total_possible_combos))

# print(all_possible_combinations)

# (Deprecated)
# all_possible_combinations_int = []
# for word_combo in all_possible_combinations:
#     to_be_added = []
#     for word in word_combo:
#         to_be_added.append(mnemonics_all.index(word) + 1)
#     all_possible_combinations_int.append(to_be_added)


# Cartesian product of possible combos
possibilities = itertools.product(*all_possible_combinations)

# Getting prepared to be filtered (delete repetitions)
possibilities_filtered = []
is_filtering = True
filter_count = 0
time_filter_started = time.time()
latest_filter_count = 0


def check_filter():
    # This thread reports progress of filtering
    global latest_filter_count
    time.sleep(10)
    while True:
        if is_filtering:
            time.sleep(1)
            time_elapsed = time.time() - time_filter_started
            speed_per_sec = (filter_count - latest_filter_count) / 10
            time_remaining = (unfiltered_possible_combos - filter_count) / speed_per_sec
            percentage = int((filter_count / unfiltered_possible_combos) * 100)
            print("{0} Found, {1}% Scanned, {2}/s (Elapsed: {3}, Remaining: {4})".format(
                len(possibilities_filtered), percentage, si_format(speed_per_sec),
                prettify_time(int(time_elapsed)), prettify_time(int(time_remaining))
            ))
            latest_filter_count = filter_count
            time.sleep(9)
        else:
            break


# Starting thread
check_thread = Thread(target=check_filter, daemon=True).start()

# Finally, filtering
for possibility in possibilities:
    if len(possibility) == len(set(possibility)):
        # print(possibility)
        possibilities_filtered.append(possibility)
    filter_count += 1

# Shutdown check_filter() thread
is_filtering = False

print("Filtered")
print("Probabilities found (filtered, without repetitions): ", len(possibilities_filtered))
print("Writing data...")

# Writing filtered possible combos (additional checkpoint)
# with open("possibilities.out.txt", "w") as f:
#     f.write(json.dumps(possibilities_filtered))

print("Validating harvested phrases...\n")

# Getting prepared to be filtered by bip39 function
valid_mnemonics = []

for mnemonic_phrase in possibilities_filtered:
    # BIP-39 Filtering
    try:
        bip39.entropy_from_mnemonic(" ".join(mnemonic_phrase), "en")
        valid_mnemonics.append(mnemonic_phrase)
        print("Found valid BIP39 - ({0}/{1})".format(len(valid_mnemonics), len(possibilities_filtered)), end="\r")
    except ValueError:
        pass

# Write BIP-39 valid mnemonics
with open("valid_possibilities.out.txt", "w") as f:
    f.write(json.dumps(valid_mnemonics))

# Done
print("Found {0} valid mnemonics".format(len(valid_mnemonics)))
