# Verb Pattern Matcher Web App

The Verb Pattern Matcher is a web application that helps users identify verb patterns and validate sentences based on those patterns. It allows users to enter a verb, see its corresponding patterns, and then test sentences to check if they match the patterns.

## Features

- Enter a verb to see its associated patterns.
- Input a sentence and validate whether it matches the selected verb's patterns.

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