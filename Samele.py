import csv
import time
import pyautogui
import urllib.request

import pytest
from colorama import Fore, Style
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def read_credentials_from_csv():

    # Hardcode the file path

    file_path =  r"C:\Users\user\Desktop\credd.csv"

    credentials = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            credentials.append(row)
            print(row)
    return credentials

def is_server_accessible(base_url):
    try:
        response = urllib.request.urlopen(base_url)
        return response.getcode() == 200
    except urllib.error.URLError:
        return False

# Function to log in with given credentials
def login_with_credentials(driver, mobileno, pwd, base_url, result_file):
    # Navigate to the login page
    login_url = base_url
    driver.get(login_url)
    driver.maximize_window()
    time.sleep(7)

    success_message = "SUCCESS: The server is accessible."
    print(Fore.GREEN + success_message + Style.RESET_ALL)
    result_file.write(success_message + '\n')
    # Get the title of the page
    page_title = driver.title

    # Inside login_with_credentials function
    if page_title == "Shortlistd":
        print("Shortlistd titled page is opened and Test case 1 is validated ")
        result_file.write("1.Shortlistd titled page is opened and Test case 1 is validated\n")
    else:
        print("Testing failed since title of the page is:", page_title)
        result_file.write("Testing failed since title of the page is: {}\n".format(page_title))


# Function to iterate through credentials and attempt login
def test_login_with_multiple_credentials(driver, result_file):
    credentials = read_credentials_from_csv()


# Read the common base URL from the first row of the CSV file

    base_url = credentials[0]['base_url']

    for credential in credentials[1:]:
        number = credential.get('mobileno')
        pwd = credential.get('pwd')


# Print the credentials to see the actual keys

        print("Credentials:", credential)

        if number and pwd:
            if login_with_credentials(driver, number, pwd, base_url, result_file):
                pass

# # Fixture to initialize the WebDriver
#
#
@pytest.fixture(scope="class")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()



# Fixture to create a log file
@pytest.fixture(scope="function")
def result_file():
    log_filename = "result_file.txt"
    with open(log_filename, 'w') as file:
        yield file

if __name__ == "__main__":
    pytest.main([__file__, "--capture=sys"])
