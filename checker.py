from selenium import webdriver
import json
import time


# P.S. This is the most amusing checker you have ever seen (maybe)

# Initializing Selenium Chrome WebDriver
driver = webdriver.Chrome()

# BIP-39 Password
password = None
# I thought mnemonic phrase was with password
# password = "Mary2701985" # Only one password shown in video

# Opening valid possibilities file, produced by main.py script
with open("valid_possibilities.out.txt", "r") as f:
    accounts_to_check = json.loads(f.read())

# If you need to skip use this
# accounts_to_check = accounts_to_check[94:]
total_accounts = len(accounts_to_check)

print("Loaded {0} accounts. Running checks...".format(total_accounts))

for index, mnemonic_phrase in enumerate(accounts_to_check):
    txn_count = None
    # While we not achieved result
    while not txn_count:
        try:
            mnemonic = " ".join(mnemonic_phrase)
            driver.get("https://iancoleman.io/bip39")
            elem = driver.find_element_by_id("phrase")
            elem.send_keys(mnemonic)

            # If password was supplied (near line 12), apply it
            if password:
                password_input = driver.find_element_by_xpath('//*[@id="passphrase"]')
                password_input.send_keys(password)
                time.sleep(1)

            # Choose BIP-49 derivation
            driver.find_element_by_id("bip49-tab").click()
            time.sleep(0.5)

            # Open CSV tab
            driver.find_element_by_id("csv-tab").click()
            time.sleep(0.5)

            # Refresh entries until we get segwit address
            first_account = "1"
            while first_account[0] != "3":
                driver.find_element_by_id("bip49-tab").click()
                try:
                    csv_accounts = driver.find_element_by_xpath('//*[@id="csv"]/div/textarea').get_attribute("value")
                    first_account = csv_accounts.split("\n")[1].split(",")[1]
                except Exception as e:
                    # If Ctrl+C is pressed
                    if e == KeyboardInterrupt:
                        exit()
                    time.sleep(1)

            print("({0}/{1}) Checking account ".format(index + 1, total_accounts) + first_account, end="... ")

            # Making request to blockchain.com
            driver.get("https://www.blockchain.com/btc/address/" + first_account)

            # Getting transaction count
            txn_count = driver.find_element_by_xpath(
                '//*[@id="__next"]/div[4]/div/div[3]/div[1]/div[1]/div[2]/div/div[3]/div[2]/span'
            ).get_attribute("innerHTML")
            print("{0} Txns".format(txn_count))

            # If we have more than 0 transactions
            if int(txn_count) > 0:
                # We've cracked it successfully
                print("Cracked successfully!")
                print(mnemonic)
                driver.close()
                exit()
        except Exception as e:
            # If we've cracked it
            if e == KeyboardInterrupt:
                exit()

            # Print message
            print("({0}/{1} Error!)".format(index + 1, total_accounts))


driver.close()
