from functional import seq
import spacy

_NER = spacy.load("en_core_web_sm")


def get_maximal_entity_cooccurrence_set(text: str):
    entity_sets = (
        _split_by_sentence_and_new_lines(text)
        .map(_get_spacy_NER_output)
        .map(_get_entities)
        .map(_filter_by_NER_type)
        .map(_get_entity_set)
        .to_list()
    )

    return _maximal_entity_cooccurrence_set_from_entity_sets(entity_sets)


def _split_by_sentence_and_new_lines(text: str):
    return (
        seq(text.split("\n"))
        .flat_map(lambda para: para.split(". "))
        .filter(lambda sentence: sentence)
        .map(lambda sentence: sentence.strip())
    )


def _get_spacy_NER_output(text_segment: str):
    return _NER(text_segment)


def _get_entities(ner_output):
    return ner_output.ents


def _filter_by_NER_type(entities):
    excluded_types = [
        "ORDINAL",
        "DATE",
        "CARDINAL",
        "QUANTITY",
        "TIME",
        "MONEY",
        "PERCENT",
    ]
    return list(filter(lambda entity: entity.label_ not in excluded_types, entities))


def _get_entity_set(entities):
    return frozenset(map(lambda entity: str(entity), entities))


def _dedupe(ls: list):
    return list(dict.fromkeys(ls))


def _maximal_entity_cooccurrence_set_from_entity_sets(
    entity_sets: list[frozenset[str]],
):
    set_lengths = list(set(len(s) for s in entity_sets))
    set_lengths.sort()
    dict_by_len = {
        l: _dedupe([s for s in entity_sets if len(s) == l]) for l in set_lengths
    }  # de-duplicate entries

    maximal_entity_cooccurrence_set: list[list[str]] = []
    for i in set_lengths:
        maximal_entity_cooccurrence_set = maximal_entity_cooccurrence_set + [
            list(s)
            for s in dict_by_len[i]
            if not any(
                [
                    s.issubset(
                        other_set
                    )  # s is not the subset of any set with length j > i
                    for j in set_lengths
                    if j > i
                    for other_set in dict_by_len[j]
                ]
            )
        ]
    return maximal_entity_cooccurrence_set
