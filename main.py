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


def prettify_time(secs):
    if secs <= 60:
        precision = 1
    else:
        precision = 2
    time_future = datetime.datetime.now() + datetime.timedelta(seconds=secs)
    prettified_time = ago.human(time_future, future_tense="{}", precision=precision)
    return prettified_time


with open("dictdata/english.txt", "r") as f:
    mnemonics_all = f.read().split("\n")[:-1]

mnemonics = ["hockey", "offer", "pact", "coffee", "leader", "design", "eyebrow", "trumpet", "word", "toddler", "tackle",
             "jacket", "unveil", "slab", "stumble", "series", "again", "theory", "maid", "salad", "guide",
             "accident", "aware", "short"]

for word in mnemonics:
    if word not in mnemonics_all:
        print("NOT VALID MNEMONICS")
        exit()

hints = [
    "u", "o", "t", "l", "w", "m", "a", "a", "c", "s", "s", "s", "t", "h", "e", "t", "j", "a", "s", "d", "s", "p", "t",
    "g"
]

# hints = [x[0] for x in mnemonics][:-2] + [""]*2
print(hints)

possible_mnemonics = mnemonics.copy()

unknown_words_possibillities = []
hint_chars = {}
unknown_hints = 0
for hint_char in hints:
    if hint_char != "" and len(hint_char) == 1:
        if hint_char not in hint_chars:
            hint_chars[hint_char] = 0
        hint_chars[hint_char] += 1
    elif hint_char == "":
        unknown_hints += 1

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
        pass
        # raise(Exception("Mnemonics aren't matched with hints"))


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

# with open("payload.out.txt", "w") as f:
#     f.write(json.dumps(all_possible_combinations))

num_possible_combos = [len(x) for x in all_possible_combinations]
print(num_possible_combos)
total_possible_combos = []
for x in num_possible_combos:
    if x == 1:
        total_possible_combos.append(x)
    elif 1 < x < len(mnemonics_if_null) or (unknown_hints == 0 and x > 1):
        total_possible_combos.append(x - 1)
    elif x == len(mnemonics_if_null):
        total_possible_combos.append(x - (unknown_hints - 1))
    else:
        raise (Exception(x, len(mnemonics_if_null), unknown_hints))

total_possible_combos = numpy.prod(total_possible_combos)
unfiltered_possible_combos = numpy.prod(num_possible_combos)
print("Total combos: {0}".format(total_possible_combos))
print("Unfiltered total combos: {0}".format(unfiltered_possible_combos))
print(all_possible_combinations)

all_possible_combinations_int = []
for word_combo in all_possible_combinations:
    to_be_added = []
    for word in word_combo:
        to_be_added.append(mnemonics_all.index(word) + 1)
    all_possible_combinations_int.append(to_be_added)

possibilities = itertools.product(*all_possible_combinations)

possibilities_filtered = []
is_filtering = True
filter_count = 0
time_filter_started = time.time()
latest_filter_count = 0


def check_filter():
    global latest_filter_count
    time.sleep(10)
    while True:
        if is_filtering:
            time.sleep(1)
            time_elapsed = time.time() - time_filter_started
            speed_per_sec = (filter_count - latest_filter_count) / 10
            time_remaining = (unfiltered_possible_combos - filter_count) / speed_per_sec
            percentage = int((filter_count / unfiltered_possible_combos) * 100)
            print("{0} Found, {1}% Scanned, {2} per sec (Elapsed: {3}, Remaining: {4})".format(
                len(possibilities_filtered), percentage, si_format(speed_per_sec),
                prettify_time(int(time_elapsed)), prettify_time(int(time_remaining))
            ))
            latest_filter_count = filter_count
            time.sleep(9)
        else:
            break


check_thread = Thread(target=check_filter, daemon=True).start()

for possibility in possibilities:
    if len(possibility) == len(set(possibility)):
        # print(possibility)
        possibilities_filtered.append(possibility)
    filter_count += 1

is_filtering = False

print("Filtered")
print("Probabilities found (filtered, without matches): ", len(possibilities_filtered))
print("Writing data...")
with open("possibilities.out.txt", "w") as f:
    f.write(json.dumps(possibilities_filtered))

print("Validating harvested phrases...\n")

valid_mnemonics = []
for mnemonic_phrase in possibilities_filtered:
    try:
        bip39.entropy_from_mnemonic(" ".join(mnemonic_phrase), "en")
        valid_mnemonics.append(mnemonic_phrase)
        print("Found valid BIP39 - ({0}/{1})".format(len(valid_mnemonics), len(possibilities_filtered)), end="\r")
    except ValueError:
        pass

with open("valid_possibilities.out.txt", "w") as f:
    f.write(json.dumps(valid_mnemonics))

print("Found valid {0} valid mnemonics".format(len(valid_mnemonics)))
