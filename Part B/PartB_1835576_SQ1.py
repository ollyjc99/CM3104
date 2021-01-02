import sys
import spacy
import json


def main(file):
    nlp = spacy.load("en_core_web_sm")

    captions, tp, fp, fn = get_metrics(nlp, file)

    for c in captions:
        print('Caption: {}, Toponym: {}'.format(c["caption"], c["feature"]))

    precision = tp / (tp + fp)
    recall = tp / (tp + fp + fn)
    f1 = 2 * precision * recall / (precision + recall)

    print('TP: {}, FP: {}, FN: {}'.format(tp, fp, fn))
    print('Precision = {:.2f}'.format(precision))
    print('Recall = {:.2f}'.format(recall))
    print('F1 = {:.2f}'.format(f1))


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

            captions.append({"caption": caption.strip(), "feature": feature})

    return captions, tp, fp, fn


def get_geographical_feature(doc):
    for ent in doc.ents:
        if ent.label_ == 'FAC' or ent.label_ == 'GPE' or ent.label_ == 'LOC':
            return ent.text.strip()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main('json-capLatLong.json')
