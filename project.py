import sqlite3
import spacy
import re


def main():
    """
    Prompts the user to enter their verb, printing its patterns.
    Then, prompts the user again to write a sentence based on the patterns printed above.
    Finally, tells the user whether their usage of a pattern is correct or not.
    """
    filename = "patterns.db"

    while True:
        verb = input("Write the base form of the verb you want to see patterns for: ").replace("to ", "").strip().lower()
        patterns = find_verb_patterns(verb, filename)
        if not patterns:
            print("Verb not found in the list. Perhaps you've misspelled it or written a different form?")
        else:
            break
    print(patterns)
    nlp = spacy.load("en_core_web_sm")

    while True:
        try:
            sentence = input("Write a phrase or a sentence using one of the patterns above: ").strip()
            doc = nlp(sentence)
            verb_ind = find_verb_index(doc, verb)
            sentence_tokens = sentence_tokenizer(doc)[verb_ind:]
            pattern_tokens = pattern_tokenizer(pattern_replacer(patterns), verb, nlp)
            print(result := matcher(sentence_tokens, pattern_tokens))
            if not result.endswith(":("):
                break
        except ValueError:
            print("It seems like you've written a sentence with a different verb. Try again?")
        except KeyboardInterrupt:
            print("\nRun it again to try another verb!")
            break


def find_verb_patterns(verb: str, filename: str) -> str | None:
    """ Opens the database and if the verb is there, returns its patterns """
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    cursor.execute("SELECT patterns FROM verb_patterns WHERE verbs=?", (verb,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0].replace(', ', '\n')


def sentence_tokenizer(doc) -> list:
    """
    Creates spaCy tokens for every word in the sentence.
    If the user's verb is not the main verb of the sentence, or not a verb at all, raises an error.
    Returns a list of tokens which are present in the base_deps set starting from the main verb.
    """
    # The main basic dependencies that are present in the patterns
    base_deps = {"ROOT", "nsubj", "xcomp", "ccomp", "pcomp", "dobj",
                 "pobj", "mark", "oprd", "aux", "prep", "attr", "prt", "dative"}
    # If a word is not in base_deps (adjectives, adverbs, articles, etc.), it's not added
    tokens = [token for token in doc if token.dep_ in base_deps]
    return tokens


def find_verb_index(doc, verb: str) -> int:
    """
    Find the verb lemma in doc (the tokenized sentence) and compare it to the input verb.
    Return the index of the verb in the sentence.
    """
    modals = ["must", "may", "might", "can", "could", "shall", "should", "will", "would"]
    for i, token in enumerate(doc):
        if token.lemma_ == verb and (token.dep_ == "ROOT" or verb in modals):
            return i


def pattern_tokenizer(patterns: str, verb: str, nlp) -> list[list]:
    """ Returns a nested list of tokens based on each pattern of the verb. """
    pattern_tokens = []
    for pattern in patterns.replace(' / ', f"\n{verb} ").split("\n"):
        doc = nlp(pattern)
        pattern_tokens.append([token for token in doc])
    return pattern_tokens


def pattern_replacer(patterns: str) -> str:
    """ Replaces shortened words from patterns into their full forms, so that spaCy can recognize what they are. """
    replacements = {
        " sb/sth ": " somebody ",
        "sb": "somebody",
        " sth": " something",
        "what + clause": "what somebody does",
        "+ clause": "somebody does something",
        "...": "",
    }
    # Get rid of all parentheses and everything in them
    patterns = re.sub(r"[(].*[)]", "", patterns)

    for key, value in replacements.items():
        patterns = patterns.replace(key, value)
    return patterns


def matcher(sentence: list, patterns: list[list]) -> str:
    """ Tries to find a match of the sentence tokens with one of the patterns' tokens. """
    for pattern in patterns:
        for ind, (sen_token, pat_token) in enumerate(zip(sentence[:len(pattern)], pattern)):
            # Some exceptional conditions that don't get picked up by spaCy by default.
            if pat_token.tag_ != sen_token.tag_ and (pat_token.tag_ == "VBG" or sen_token.tag_ == "VBG"):
                break
            # "help me to get this" vs "help me to do this"
            elif pat_token.dep_ == "nsubj" and sen_token.dep_ in ["nsubj", "dobj"]:
                continue
            elif pat_token.dep_ == "ccomp" and sen_token.dep_ in ["ccomp", "xcomp"]:
                continue
            # doing/do (something)
            elif ind == len(pattern) - 1 and pattern[ind - 1].tag_ in ["VBG", "VB"]:
                continue
            # base case - if their dependencies are different
            elif sen_token.dep_ != pat_token.dep_:
                break
            # same dependencies, but different prepositions
            elif pat_token.dep_ == "prep" and pat_token.lemma_ != sen_token.lemma_:
                break
        else:
            return "The usage of one of the patterns with this verb is correct!"
    return "This seems to be incorrect :("


if __name__ == "__main__":
    main()
