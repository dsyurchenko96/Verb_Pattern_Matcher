from flask import Flask, render_template, request, session
import spacy
from project import find_verb_patterns, sentence_tokenizer, find_verb_index, \
    pattern_tokenizer, pattern_replacer, matcher

app = Flask(__name__)
app.config['SECRET_KEY'] = "6eda7656a0ee25bb07f65d5dce819017"
DATABASE = 'patterns.db'


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    The user inputs the verb, the webpage displays the patterns from the database and saves
    both of these parameters for the validation of the sentence in the validate_sentence function.
    """
    if request.method == 'POST':
        verb = request.form.get('verb').lower().strip().replace("to ", "")
        patterns = find_verb_patterns(verb, DATABASE)
        if patterns is None:
            verb_not_found_error = "Verb not found in the list. " \
                            "Perhaps you've misspelled it or written a different form?"
            return render_template('index.html', verb_not_found_error=verb_not_found_error)
        session['verb'] = verb
        session['patterns'] = patterns
        return render_template('index.html', patterns=patterns, verb=verb)

    # Display the original welcome page with the verb input field
    return render_template('index.html')


@app.route('/validate', methods=['POST'])
def validate_sentence():
    """ Using project.py functions, the sentence is validated. """
    verb = session.get('verb')
    patterns = session.get('patterns')
    sentence = request.form.get('sentence')

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)
    sentence_tokens = sentence_tokenizer(doc)
    verb_ind = find_verb_index(sentence_tokens, verb)
    if verb_ind is None:
        verb_ind_error = "It seems like you've written a sentence with a different verb. Try again?"
        return render_template('index.html', patterns=patterns, verb=verb, verb_ind_error=verb_ind_error)
    tokens_from_root = sentence_tokens[verb_ind:]
    pattern_tokens = pattern_tokenizer(pattern_replacer(patterns), verb, nlp)
    result = matcher(tokens_from_root, pattern_tokens)

    return render_template('index.html', patterns=patterns, verb=verb, sentence_result=result)


if __name__ == '__main__':
    app.run()
