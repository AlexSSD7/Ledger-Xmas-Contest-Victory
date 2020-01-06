import json

import blockcypher
from bip32utils import BIP32Key
from bip32utils import BIP32_HARDEN
from btclib import bip39

# Opening valid possibilities file, produced by main.py script
with open("valid_possibilities.out.txt", "r") as f:
    accounts_to_check = json.loads(f.read())

# If you need to skip use this
# accounts_to_check = accounts_to_check[94:]

print(f"Loaded {len(accounts_to_check)} accounts. Running checks...")

addresses = {}
print("Deriving addresses")
for possibility in accounts_to_check:
    str_poss = ' '.join(possibility)
    seed = bip39.seed_from_mnemonic(str_poss, "")  # Converting mnemonic to BIP39 Seed
    key = BIP32Key.fromEntropy(seed)  # Converting to BIP32 Root Key
    account_number = 0  # This variable can be changed to attain a different derivation path
    i = 0               # This variable can be changed to attain a different derivation path
    # For the following account derivation, `BIP32_HARDEN` can be simply removed to access unhardened addresses
    addr = key.ChildKey(49 + BIP32_HARDEN) \
        .ChildKey(0 + BIP32_HARDEN) \
        .ChildKey(account_number + BIP32_HARDEN) \
        .ChildKey(0) \
        .ChildKey(i) \
        .P2WPKHoP2SHAddress()
    addresses[addr] = str_poss

print(f"{len(addresses)} addresses derived.")
for address in addresses:
    print(f"Checking address {address}")
    if blockcypher.get_total_num_transactions(address) > 0:
        print(f'The correct address is {address}\nThe correct mnemonic is: \n{addresses[addr]}')
        quit()
