import spacy
import json
import argparse


def main(file):
    nlp = spacy.load("en_core_web_sm")
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
            print('Caption: {}, Toponym: {}'.format(caption, feature))
        print('TP: {}, FP: {}, FN: {}'.format(tp, fp, fn))
        precision = tp / (tp + fp)
        print('Precision = {:.2f}'.format(precision))
        recall = tp / (tp + fp + fn)
        print('Recall = {:.2f}'.format(recall))

        print('F1 = {:.2f}'.format(2 * precision * recall / (precision + recall)))


def get_metrics(nlp, file):
    captions = []
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

            captions.append({"caption": caption, "feature": feature})

    return captions, tp, fp, fn


def get_geographical_feature(doc):
    for ent in doc.ents:
        if ent.label_ == 'FAC' or ent.label_ == 'GPE' or ent.label_ == 'LOC':
            return ent.text.strip()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Arguments')
    parser.add_argument('json_file', type=str, help='Path for JSON file')
    args = parser.parse_args()
    main(args.json_file)
