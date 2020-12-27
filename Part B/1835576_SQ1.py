import spacy

nlp = spacy.load("en_core_web_sm")

text = ("Apple shift insurance liability toward manufacturers")
doc = nlp(text)

for token in doc.ents:
    print(token.text, token.label_)
