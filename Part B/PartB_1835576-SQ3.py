import sys
import spacy
import json
import random
from geopy.geocoders import Nominatim
from geopy.distance import geodesic


def main(file):

    nlp = get_new_model()

    captions, tp, fp, fn = get_metrics(nlp, file)

    for c in captions:
        print('Full Address: {address}'.format(address=c["full address"]))
        print(
            'Coordinates: ({coords[0]:.2f},{coords[1]:.2f}), Distance: {distance:.2f}km'.format(
                coords=c["coordinates"], distance=c["distance"]
            )
        )

    precision = tp / (tp + fp)
    recall = tp / (tp + fp + fn)
    f1 = 2 * precision * recall / (precision + recall)

    print('TP: {}, FP: {}, FN: {}'.format(tp, fp, fn))
    print('Precision = {:.2f}'.format(precision))
    print('Recall = {:.2f}'.format(recall))

    print('F1 = {:.2f}'.format(f1))


def get_metrics(nlp, file):
    captions = []
    geolocator = Nominatim(user_agent="coursework-ner-geocoder")
    with open(file) as json_file:
        data = json.load(json_file)
        tp, fp, fn = 0, 0, 0
        for p in data:
            caption = p['caption']
            feature = get_geographical_feature(nlp(caption))
            location = geolocator.geocode(feature, language="en", limit=1)
            if location:
                guide_coords = (
                    round(float(p["guide-latitude-WGS84"]), 2),
                    round(float(p["guide-longitude-WGS84"]), 2)
                )
                retrieved_coords = (
                    round(location.latitude, 2),
                    round(location.longitude, 2)
                )
                distance = geodesic(guide_coords, retrieved_coords).km
                if distance <= 20:
                    tp += 1
                else:
                    fp += 1
            else:
                fn += 1

            captions.append({
                "full address": location.address.strip(),
                "coordinates": (location.latitude, location.longitude),
                "distance": distance})

    return captions, tp, fp, fn


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
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main('json-capLatLong.json')
