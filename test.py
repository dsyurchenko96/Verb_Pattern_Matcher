from project import find_verb_patterns, find_verb_index, pattern_replacer, sentence_tokenizer, pattern_tokenizer, matcher
import spacy

filename = "patterns.db"
nlp = spacy.load("en_core_web_sm")


def test_find_verb():
    assert find_verb_patterns("abstain", filename) == "abstain from doing sth"
    assert find_verb_patterns("accuse", filename) == "accuse sb of doing sth"
    assert find_verb_patterns("advocate", filename) == "advocate doing sth\nadvocate sb('s) doing sth" \
                                                       "\nadvocate that + clause"
    assert find_verb_patterns("attempt", filename) == "attempt doing sth / to do sth (no real difference)"
    assert find_verb_patterns("askkfdfweef", filename) is None
    assert find_verb_patterns("heeelp", filename) is None
    assert find_verb_patterns("123", filename) is None
    assert find_verb_patterns("he", filename) is None


def test_find_verb_index():
    assert find_verb_index(nlp("Can you help me to find the way?"), "help") == 2
    assert find_verb_index(nlp("I abstain from writing tests myself!"), "abstain") == 1
    assert find_verb_index(nlp("You definitely deserve to get a rest"), "deserve") == 2
    assert find_verb_index(nlp("I need your help with this one"), "help") is None


def test_pattern_replacer():
    assert pattern_replacer("abstain from doing sth") == "abstain from doing something"
    assert pattern_replacer("deem sb/sth to be sth") == "deem somebody to be something"
    assert pattern_replacer("advocate doing sth\nadvocate sb('s) doing sth\nadvocate that + clause") \
           == "advocate doing something\nadvocate somebody doing something\nadvocate that somebody does something"


def test_matcher():
    verb = "abstain"
    patterns = pattern_tokenizer("abstain from doing something", verb, nlp)
    doc = nlp("I abstain from writing tests myself!")
    sentence_tokens = sentence_tokenizer(doc)
    verb_ind = find_verb_index(sentence_tokens, verb)
    tokens_from_root = sentence_tokens[verb_ind:]
    assert matcher(tokens_from_root, patterns) == "The usage of one of the patterns with this verb is correct!"

    doc = nlp("I abstain write tests myself!")
    sentence_tokens = sentence_tokenizer(doc)
    verb_ind = find_verb_index(sentence_tokens, verb)
    tokens_from_root = sentence_tokens[verb_ind:]
    assert matcher(tokens_from_root, patterns) == "This seems to be incorrect :("

    verb = "debate"
    patterns = pattern_tokenizer("debate what to do / what somebody does"
                                 "\ndebate whether to do something / whether somebody does something",
                                 verb, nlp)
    doc = nlp("She debates whether to eat cake or not")
    sentence_tokens = sentence_tokenizer(doc)
    verb_ind = find_verb_index(sentence_tokens, verb)
    tokens_from_root = sentence_tokens[verb_ind:]
    assert matcher(tokens_from_root, patterns) == "The usage of one of the patterns with this verb is correct!"

    doc = nlp("She debates eating the cake")
    sentence_tokens = sentence_tokenizer(doc)
    verb_ind = find_verb_index(sentence_tokens, verb)
    tokens_from_root = sentence_tokens[verb_ind:]
    assert matcher(tokens_from_root, patterns) == "This seems to be incorrect :("

    verb = "aim"
    patterns = pattern_tokenizer("aim to do something\naim at doing something", verb, nlp)
    doc = nlp("I aim creating the best program ever!")
    sentence_tokens = sentence_tokenizer(doc)
    verb_ind = find_verb_index(sentence_tokens, verb)
    tokens_from_root = sentence_tokens[verb_ind:]
    assert matcher(tokens_from_root, patterns) == "This seems to be incorrect :("

    doc = nlp("I aim to create the best program ever!")
    sentence_tokens = sentence_tokenizer(doc)
    verb_ind = find_verb_index(sentence_tokens, verb)
    tokens_from_root = sentence_tokens[verb_ind:]
    assert matcher(tokens_from_root, patterns) == "The usage of one of the patterns with this verb is correct!"

