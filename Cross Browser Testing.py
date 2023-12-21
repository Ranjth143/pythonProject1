import csv
import time
import urllib.request
import pytest
from colorama import Fore, Style
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def read_credentials_from_csv():
    file_path = r"C:\Users\user\Desktop\credd.csv"
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
    time.sleep(2)

    success_message = "SUCCESS: The server is accessible."
    print(Fore.GREEN + success_message + Style.RESET_ALL)
    result_file.write(success_message + '\n')
    # Get the title of the page
    page_title = driver.title

    # Print or use the title as needed
    print("Page Title:", page_title)
    if page_title == "Facebook – log in or sign up":
        print("Facebook titled page is opened and Test case 1 is validated ")
        result_file.write("1.Facebook titled page is opened and Test case 1 is validated\n")
    else:
        print("Testing fialed since title of the page is :", page_title )
        result_file.write("Testing fialed since title of the page is :", page_title,'\n')

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
            if driver.name == 'chrome':
                print("Executing on Chrome browser")
                # Call your login function for Chrome
                login_with_credentials(driver, number, pwd, base_url, result_file)
            elif driver.name == 'firefox':
                print("Executing on Firefox browser")
                # Call your login function for Firefox
                login_with_credentials(driver, number, pwd, base_url, result_file)
            # Add more conditions for other browsers as needed

# Fixture to initialize the WebDriver for Chrome
@pytest.fixture(scope="class")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


@pytest.fixture(scope="class")
def chrome_driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

# Fixture to initialize the WebDriver for Firefox
@pytest.fixture(scope="class")
def firefox_driver():
    driver = webdriver.Firefox()
    yield driver
    driver.quit()

# Fixture to create a log file
@pytest.fixture(scope="function")
def result_file():
    log_filename = "result_file.txt"
    with open(log_filename, 'w') as file:
        yield file

# Test case using Chrome
def test_login_with_multiple_credentials_chrome(chrome_driver, result_file):
    test_login_with_multiple_credentials(chrome_driver, result_file)

# Test case using Firefox
def test_login_with_multiple_credentials_firefox(firefox_driver, result_file):
    test_login_with_multiple_credentials(firefox_driver, result_file)

if __name__ == "__main__":
    pytest.main([__file__, "--capture=sys"])