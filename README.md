# Ledger Xmas Contest
Hey there, i'm so exited about my victory on this contest. Proud to share my code. I made it as one-time script, so please, don't judge strictly.

### Hint
![hint](https://www.ledger.com/wp-content/uploads/2019/12/recoveryBlog.png)


### Cracked mnemonic phrase
```
unveil offer trumpet leader word maid again accident coffee series slab salad theory hockey eyebrow toddler jacket aware short design stumble pact tackle guide
```

You can view this account on [exporer](https://www.blockchain.com/btc/address/3JeVd5ALNDvn7BbkqLYfV4qeQ16guPwJD2).

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
['u', 'o', 't', 'l', 'w', 'm', 'a', 'a', 'c', 's', 's', 's', 't', 'h', 'e', 't', 'j', 'a', 's', 'd', 's', 'p', 't', 'g']
[1, 1, 4, 1, 1, 1, 3, 3, 1, 5, 5, 5, 4, 1, 1, 4, 1, 3, 5, 1, 5, 1, 4, 1]
Total combos: 663552
Unfiltered total combos: 21600000
[['unveil'], ['offer'], ['trumpet', 'toddler', 'tackle', 'theory'], ['leader'], ['word'], ['maid'], ['again', 'accident', 'aware'], ['again', 'accident', 'aware'], ['coffee'], ['slab', 'stumble', 'series', 'salad', 'short'], ['slab', 'stumble', 'series', 'salad', 'short'], ['slab', 'stumble', 'series', 'salad', 'short'], ['trumpet', 'toddler', 'tackle', 'theory'], ['hockey'], ['eyebrow'], ['trumpet', 'toddler', 'tackle', 'theory'], ['jacket'], ['again', 'accident', 'aware'], ['slab', 'stumble', 'series', 'salad', 'short'], ['design'], ['slab', 'stumble', 'series', 'salad', 'short'], ['pact'], ['trumpet', 'toddler', 'tackle', 'theory'], ['guide']]
16020 Found, 92% Scanned, 2.0 M per sec (Elapsed: 10 seconds, Remaining: 1.329 milliseconds ago)
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

That's all!

> python3 <3