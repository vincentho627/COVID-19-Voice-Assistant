import spacy

nlp = spacy.load("en_core_web_sm")


def extractCountry(sentence):
    doc = nlp(sentence)
    for token in doc.ents:
        if token.label_ == 'GPE':
            return token.text

    return ""
