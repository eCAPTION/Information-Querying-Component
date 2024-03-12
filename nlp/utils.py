from functional import seq
from refined.inference.processor import Refined

refined = Refined.from_pretrained(model_name="wikipedia_model", entity_set="wikipedia")


def get_maximal_entity_cooccurrence_set(text: str):
    entity_sets = (
        _split_by_sentence_and_new_lines(text)
        .map(_get_named_entity_linking_entity_ids)
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


def _get_named_entity_linking_entity_ids(text_segment: str):
    spans = refined.process_text(text_segment)
    entity_ids = [
        int(span.predicted_entity.wikidata_entity_id[1:])
        for span in spans
        if span.predicted_entity.wikidata_entity_id != None
    ]
    return entity_ids


def _get_entity_set(entities):
    return frozenset(entities)


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
