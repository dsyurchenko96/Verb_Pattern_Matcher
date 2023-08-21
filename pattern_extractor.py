from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import sqlite3


def main():
    url = "http://random-idea-english.blogspot.com/p/verb-patterns.html"
    filename = "patterns.db"
    database_name = "verb_patterns"
    verb_patterns = extract_patterns(url)
    try:
        create_database(database_name, filename, verb_patterns)
    except ValueError:
        print(f"{filename} already exists!")


def extract_patterns(url: str) -> list[dict]:
    """
    Launches the Chrome webdriver, goes to the url and finds the drop-down menu. Then, clicks through every verb
    and saves the verb and its patterns in a list of dictionaries.
    """
    driver = webdriver.Chrome()
    driver.get(url)
    select_element = driver.find_element(By.ID, "indexSelect")

    # Get the list of option elements within the "Select verb" element
    options = select_element.find_elements(By.TAG_NAME, "option")

    # Initialize the list of dictionaries to store verb patterns
    verb_patterns = []

    # Iterate through the options
    for option in options:
        verb = option.text.strip()
        if verb and verb != "Select verb":
            option.click()  # Click the option to trigger the content change

            # Extract the verb patterns
            patterns_element = driver.find_element(By.ID, "verbInfo")
            patterns = [pattern.text.strip() for pattern in patterns_element.find_elements(By.TAG_NAME, "li")[1:]]
            pattern_string = ", ".join(patterns)

            # Create a dictionary for the current verb and its patterns
            verb_dict = {"verbs": verb, "patterns": pattern_string}

            # Append the dictionary to the list
            verb_patterns.append(verb_dict)

    driver.quit()
    return verb_patterns


def create_database(database_name: str, filename: str, verb_patterns: list[dict]) -> None:
    """ Creates an SQLite database using pandas from verb_patterns. """
    df = pd.DataFrame(verb_patterns)
    con = sqlite3.connect(filename)
    df.to_sql(name=database_name, con=con, index=False)
    con.close()


if __name__ == '__main__':
    main()
