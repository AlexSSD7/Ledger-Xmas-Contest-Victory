# Ledger Xmas Contest
[![Build Status](https://travis-ci.org/AlexSSD7/Ledger-Xmas-Contest-Victory.svg?branch=master)](https://travis-ci.org/AlexSSD7/Ledger-Xmas-Contest-Victory)

Hey there, i'm so exited about my victory on this contest. Proud to share my code. I made this as one-time script, so please, don't judge strictly.

### Note
Master branch contains fixes and improvements, if you want to go with original version, please delegate to [original branch](https://github.com/AlexSSD7/Ledger-Xmas-Contest-Victory/tree/original)

### Cracked mnemonic phrase
![](assets/seed.png)

```
unveil offer trumpet leader word maid again accident coffee series slab salad theory hockey eyebrow toddler jacket aware short design stumble pact tackle guide
```

You can view this account on [explorer](https://www.blockchain.com/btc/address/3JeVd5ALNDvn7BbkqLYfV4qeQ16guPwJD2).

## How to reproduce that?
That's very simple, let's begin our journey by installing **python** dependencies.
```sh
$ pip3 install -r requirements.txt
```
Then, install **Chrome Web Driver for Selenium** [here](https://pypi.org/project/selenium/).

Good, we have python deps installed successfully, let's start automated **start.py** script.
```sh
$ python3 start.py
```

This will run the generator, and *shitty* validator after it.
```
Output:
Generating valid accounts....
Total combos (with repetitions)   : 21600000
Total combos (without repetitions): 663552
16224 Found, 93% Scanned, 2.0 M/s (Elapsed: 10 seconds, Remaining: 0.421 milliseconds)
Filtered
Probabilities found (filtered, without matches):  17280
Writing data...
Validating harvested phrases...

Found valid 69 valid mnemonics
Validating...
Loaded 69 accounts. Running checks...
(1/69) Checking account 3MPJmHQHTeH3JLBaykQUMzsS5dRA66qutQ... 0 Txns
(2/69) Checking account 3JeVd5ALNDvn7BbkqLYfV4qeQ16guPwJD2... 3 Txns
Cracked successfully!
unveil offer trumpet leader word maid again accident coffee series slab salad theory hockey eyebrow toddler jacket aware short design stumble pact tackle guide
Cleaning up...
Done.
```

Star this repo, if you found it helpful.

That's all!

Twitter: [@Sadovskyi_Alex](https://twitter.com/Sadovskyi_Alex)

> python3 <3
