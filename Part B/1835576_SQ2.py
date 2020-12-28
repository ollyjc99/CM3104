import spacy
import json
import random
import argparse


def main(file):
    # GPE = Countries, Cities, States, etc.
    # LOC = Non-GPE locations, mountain ranges, bodies of water
    # FAC = Buildings, airports, highways, bridges

    nlp = get_new_model()

    with open(file) as json_file:
        data = json.load(json_file)
        tp, fp, fn = 0, 0, 0
        for p in data:
            caption = p['caption']
            feature = get_geographical_feature(nlp(p['caption']))
            toponym = p['ground truth toponym']
            if feature:
                if feature == toponym:
                    tp += 1
                else:
                    fp += 1
            else:
                fn += 1
            print('Caption: {}, Geographical feature: {}'.format(caption, feature))

        print('TP: {}, FP: {}, FN: {}'.format(tp, fp, fn))
        precision = tp / (tp + fp)
        print('Precision = {:.2f}'.format(precision))
        recall = tp / (tp + fp + fn)
        print('Recall = {:.2f}'.format(recall))

        print('F1 = {:.2f}'.format(2 * precision * recall / (precision + recall)))


def get_geographical_feature(doc):
    for ent in doc.ents:
        if ent.label_ == 'FAC' or ent.label_ == 'GPE' or ent.label_ == 'LOC':
            return ent.text.strip()


def get_new_model():
    nlp = spacy.blank("en")
    train_data = [
        ("Grassland north of Eastdon", {
            "entities": [(19, 26, "GPE")]
        }),
        ("Wall north of Hulne Park", {
            "entities": [(14, 24, "GPE")]
        }),
        ("A45 north of South Solihull", {
            "entities": [(13, 27, "GPE")]
        })
    ]
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner, last=True)
    else:
        ner = nlp.get_pipe("ner")

    for _, annotations in train_data:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        for i in range(50):
            random.shuffle(train_data)
            for text, annotations in train_data:
                nlp.update([text], [annotations], drop=0.5, sgd=optimizer)
    return nlp


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Arguments')
    parser.add_argument('json_file', type=str, help='Path for JSON file')
    args = parser.parse_args()
    main(args.json_file)
