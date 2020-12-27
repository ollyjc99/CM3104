import spacy
import json


def main():
    nlp = spacy.load("en_core_web_sm")
    with open('json-capLatLong.json') as json_file:
        data = json.load(json_file)
        for p in data:
            print('Caption: {}, Geographical feature {}'.format(p['caption'], get_geographical_feature(nlp(p['caption']))))


def get_geographical_feature(doc):
    for ent in doc.ents:
        if ent.label_ == 'FAC' or ent.label_ == 'GPE' or ent.label_ == 'LOC':
            return ent.text.strip()


if __name__ == '__main__':
    main()
