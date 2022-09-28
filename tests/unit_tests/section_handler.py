from unittest import TestCase

from app.config.definitions import SECTION_SEPARATOR
from app.helpers.section_handler import SectionHandler


def assert_equal_dicts(x: dict, y: dict) -> bool:
    assert isinstance(x, dict)
    assert isinstance(y, dict)
    assert x.keys() & y.keys() == x.keys(), 'Missing key(s) in second dict : %s' % repr(x.keys() - y.keys())
    assert x.keys() & y.keys() == y.keys(), 'Missing key(s) in first dict : %s' % repr(y.keys() - x.keys())
    for key in x.keys():
        assert x[key] == y[key], '`%s` key has different values : %s != %s' % (key, repr(x[key]), repr(y[key]))
    return True


class TestSectionHandler(TestCase):

    def setUp(self) -> None:
        self.article_test = {"body": "Lille est une belle ville.", "title": "Nantes, belle comme Marseille"}
        self.ner_results = [
            {"text": "Lille", "startOffset": 0, "endOffset": 5},
            {"text": "Nantes", "startOffset": 26+len(SECTION_SEPARATOR), "endOffset": 32+len(SECTION_SEPARATOR)},
            {"text": "Marseille", "startOffset": 46+len(SECTION_SEPARATOR), "endOffset": 55+len(SECTION_SEPARATOR)}
        ]
        self.expected_ner_results = [
            {'text': 'Lille', 'startOffset': 0, 'endOffset': 5, 'articleSection': 'body'},
            {'text': 'Nantes',
             'startOffset': 0,
             'endOffset': 6,
             'articleSection': 'title'},
            {'text': 'Marseille',
             'startOffset': 20,
             'endOffset': 29,
             'articleSection': 'title'}
        ]
        self.entities_sections = {entity['text']: entity['articleSection'] for entity in self.expected_ner_results}

    def testDontAttributeSectionToOutsideEntity(self):
        section_handler = SectionHandler(self.article_test, sections=('body', 'title'))
        outside_entities = [{'text': 'Tokyo', 'startOffset': 1000}]
        section_handler.attribute_Section_To_Ner(outside_entities)
        for entity in outside_entities:
            self.assertFalse('articleSection' in entity)

    def testAttributeSectionToEntity(self):
        section_handler = SectionHandler(self.article_test, sections=('body', 'title'))
        ner_results = self.ner_results.copy()
        section_handler.attribute_Section_To_Ner(ner_results)
        for entity in ner_results:
            expected = [ent for ent in self.expected_ner_results if ent['text'] == entity['text']][0]
            self.assertTrue(assert_equal_dicts(entity, expected))

    def testDetectAnEntityBelongToSection(self):
        section_handler = SectionHandler(self.article_test, sections=('body', 'title'))
        for entity in self.ner_results:
            self.assertTrue(section_handler.is_entity_in_section(entity, self.entities_sections.get(entity['text'])))

    def testDetectAnEntityDoesNotBelongToSection(self):
        section_handler = SectionHandler(self.article_test, sections=('body', 'title'))
        for entity in self.ner_results:
            sections_entity_is_not_in = {'body', 'title'}
            sections_entity_is_not_in.remove(self.entities_sections.get(entity['text']))
            for section_entity_is_not_in in sections_entity_is_not_in:
                self.assertFalse(section_handler.is_entity_in_section(entity, section_entity_is_not_in))
