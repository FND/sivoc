import serialization.text as txt

from model.concept import Concept
from model.label import Label


def test_list():
    c1 = Concept("_666")
    c2 = Concept("_999")
    l1 = Label("foo", "en")
    l2 = Label("bar", "de")

    lines = txt.list_concepts([c1, c2])
    lines = "".join(lines)
    assert lines == "_666\n_999\n"

    c1.pref_labels.append(l1)

    lines = txt.list_concepts([c1, c2])
    lines = "".join(lines)
    assert lines == "foo\n_999\n"

    c1.alt_labels.append(l2)

    lines = txt.list_concepts([c1, c2])
    lines = "".join(lines)
    assert lines == "foo\n_999\n"

    c2.alt_labels.append(l1)

    lines = txt.list_concepts([c1, c2])
    lines = "".join(lines)
    assert lines == "foo\n_999\n"


def test_show():
    c0 = Concept("_666")
    l1 = Label("foo", "en")
    l2 = Label("bar", "de")

    lines = txt.show_concept(c0)
    lines = "".join(lines)
    assert lines == "_666\n\nPREFERRED LABELS\n\nALTERNATIVE LABELS\n"

    c0.pref_labels.append(l1)

    lines = txt.show_concept(c0)
    lines = "".join(lines)
    assert lines == ("_666\n\n"
            "PREFERRED LABELS\n    [en] foo\n\n"
            "ALTERNATIVE LABELS\n")

    c0.pref_labels.append(l2)

    lines = txt.show_concept(c0)
    lines = "".join(lines)
    assert lines == ("_666\n\n"
            "PREFERRED LABELS\n    [en] foo\n    [de] bar\n\n"
            "ALTERNATIVE LABELS\n")

    c0.alt_labels.append(l2)

    lines = txt.show_concept(c0)
    lines = "".join(lines)
    assert lines == ("_666\n\n"
            "PREFERRED LABELS\n    [en] foo\n    [de] bar\n\n"
            "ALTERNATIVE LABELS\n    [de] bar\n")

    c0.alt_labels.append(l1)

    lines = txt.show_concept(c0)
    lines = "".join(lines)
    assert lines == ("_666\n\nPREFERRED LABELS\n    [en] foo\n    [de] bar\n\n"
            "ALTERNATIVE LABELS\n    [de] bar\n    [en] foo\n")
