# Verb Pattern Matcher Web App

The Verb Pattern Matcher is a web application that helps users identify verb patterns and validate sentences based on those patterns. It allows users to enter a verb, see its corresponding patterns, and then test sentences to check if they match the patterns.

## Features

- Enter a verb to see its associated patterns.
- Input a sentence and validate whether it matches the selected verb's patterns.

## Description

1. **Web Scraping Verb Patterns**: (This step is only done once if the _patterns.db_ file doesn't exist yet). The program starts by accessing a specific website (http://random-idea-english.blogspot.com/p/verb-patterns.html) that contains a list of verbs and their associated patterns. It uses the Selenium library to automate web browsing, navigating through a dropdown menu to extract verb patterns for each verb.


2. **Data Storage**: Extracted verb patterns are stored in an SQLite database called _patterns.db_. This file allows the program to quickly retrieve verb patterns without repeatedly scraping the website.


3. **User Interaction**: Upon running the program, users are prompted to enter the base form of a verb they want to explore. The program then searches the database for the verb and displays its associated patterns. Users are guided to choose a pattern and construct a sentence based on it.


4. **Pattern Validation**: The program evaluates the sentence provided by the user, checking if the usage adheres to the selected pattern. It employs spaCy, an NLP library, to tokenize and analyze the sentence's structure and compare it to the selected pattern's dependencies.


5. **User Feedback**: Based on the pattern validation, the program provides feedback to the user, indicating whether their usage of the selected pattern is correct or not.

## Getting Started

1. Install the required packages listed in `requirements.txt` using the following command:
```
pip install -r requirements.txt
```
2. Run the Flask app:
```
flask run
```
3. Open your web browser and navigate to `http://127.0.0.1:5000` to access the web app.

## Usage

1. Enter a verb in the input field and click "Get Patterns" to see the corresponding patterns.
2. Enter a sentence based on the displayed patterns and click "Check Sentence" to validate it.
3. If the sentence matches the patterns, a success message will be displayed. Otherwise, an error message will appear.

## Dependencies

- Flask
- spaCy

## File Structure

- `app.py`: The Flask web app code.
- `project.py`: The script with all necessary functions for pattern checking. Can be run separately via a command-line interface.
- `templates/index.html`: HTML template for the index page.
- `patterns.db`: SQLite database containing verb patterns.


## License

This project is licensed under the [MIT License](LICENSE).