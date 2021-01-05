import spacy

nlp = spacy.load("en_core_web_sm")


def extractKeyInformation(sentence):
    doc = nlp(sentence)
    death = False       # says if we want death cases
    percent = False     # says if we want the death percentage value
    countries = []
    for token in doc.ents:
        if token.label_ == 'GPE':
            countries.append(token.text)

    lemmas = [token.lemma_ for token in sentence]

    if 'death' in lemmas or 'died' in lemmas:
        death = True
        if 'percent' in lemmas or 'percentage' in lemmas:
            percent = True

    return death, percent, countries
