from model.concept import Concept
from model.label import Label


_data = {
    "concepts": {
        "01": {
            "pref": 0,
            "alt": [1, 2]
        },
        "02": {
            "pref": 3,
            "alt": [4, 5]
        }
    },
    "labels": {
        0: { "lang": "la", "name": "sol" },
        1: { "lang": "en", "name": "sun" },
        2: { "lang": "de", "name": "Sonne" },
        3: { "lang": "la", "name": "terra" },
        4: { "lang": "en", "name": "earth" },
        5: { "lang": "de", "name": "Erde" }
    }
}


class Store(object):

    def __init__(self, concepts=None, labels=None):
        self.concepts = concepts or {}
        self.labels = labels or {}


def _load(data):
    labels = {}
    for _id, label in data["labels"].items():
        labels[_id] = Label(label["name"], label["lang"])

    concepts = {}
    for _id, concept in data["concepts"].items():
        label_id = concept["pref"]
        pref_label = labels[label_id]

        alt_labels = [labels[label_id] for label_id in concept["alt"]]

        concepts[_id] = Concept(_id, [pref_label], alt_labels)

    return Store(concepts, labels)


STORE = _load(_data)
