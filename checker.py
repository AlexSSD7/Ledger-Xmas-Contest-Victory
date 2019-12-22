from selenium import webdriver
import json
import time


# P.S. This is the most amusing checker you have ever seen (maybe)

driver = webdriver.Chrome()

# BIP-39 Password
password = None
# I thought mnemonic phrase was with pasword
# password = "Mary2701985" # Only one password shown in video

with open("valid_possibilities.out.txt", "r") as f:
    accounts_to_check = json.loads(f.read())

# If you need to skip use this
# accounts_to_check = accounts_to_check[94:]
total_accounts = len(accounts_to_check)
print("Loaded {0} accounts. Running checks...".format(total_accounts))
for index, mnemonic_phrase in enumerate(accounts_to_check):
    txn_count = None
    while not txn_count:
        try:
            mnemonic = " ".join(mnemonic_phrase)
            driver.get("https://iancoleman.io/bip39")
            elem = driver.find_element_by_id("phrase")
            elem.send_keys(mnemonic)
            if password:
                password_input = driver.find_element_by_xpath('//*[@id="passphrase"]')
                password_input.send_keys(password)
                time.sleep(1)
            driver.find_element_by_id("bip49-tab").click()
            time.sleep(0.5)
            driver.find_element_by_id("csv-tab").click()
            time.sleep(0.5)
            first_account = "1"
            while first_account[0] != "3":
                driver.find_element_by_id("bip49-tab").click()
                try:
                    csv_accounts = driver.find_element_by_xpath('//*[@id="csv"]/div/textarea').get_attribute("value")
                    first_account = csv_accounts.split("\n")[1].split(",")[1]
                except:
                    time.sleep(1)
            print("({0}/{1}) Checking account ".format(index + 1, total_accounts) + first_account, end="... ")
            driver.get("https://www.blockchain.com/btc/address/" + first_account)
            txn_count = driver.find_element_by_xpath(
                '//*[@id="__next"]/div[4]/div/div[3]/div[1]/div[1]/div[2]/div/div[3]/div[2]/span'
            ).get_attribute("innerHTML")
            print("{0} Txns".format(txn_count))
            if int(txn_count) > 0:
                print("Cracked successfully!")
                print(mnemonic)
                driver.close()
                exit()
        except Exception as e:
            raise(e)
            print("({0}/{1} Error!)".format(index + 1, total_accounts))


driver.close()
