from app.config.definitions import SECTION_SEPARATOR


class SectionHandler:
    """
    When a document is made of several sections (title, text, snippet...), it is desirable to call only once the NER
    algorithm (or other algorithm working at token level) while still being able to define at which section a detected
    object (an entity for the NER) is attached. This class provides tools to do so.
    Example:
        {"body": "Lille est une belle ville.", "title": "Nantes, belle comme Marseille"}
        self.full_text =  "Lille est une belle ville. Nantes, belle comme Marseille"

    The expected ner results would be :
         [
            {'text': 'Lille',
            'startOffset': 0,
            'endOffset': 5,
            'articleSection': 'body'
            },
            {'text': 'Nantes',
             'startOffset': 0,
             'endOffset': 6,
             'articleSection': 'title'
             },
            {'text': 'Marseille',
             'startOffset': 20,
             'endOffset': 29,
             'articleSection': 'title'
             }]
    """


    def __init__(self, article, sections=('title', 'text')):
        self._ordered_sections = sections

        self.full_text = SECTION_SEPARATOR.join(article[section] for section in self._ordered_sections)
        self._section_limits = SectionHandler.compute_sections_limits(article, self._ordered_sections)

    def attribute_Section_To_Ner(self, ner_results: list):
        """
        Take a list of entity detected from self.full_text and attribute the right section according to the StartOffset
        """
        for entity in ner_results:
            for section in self._ordered_sections:
                if self.is_entity_in_section(entity, section):
                    entity["articleSection"] = section
                    section_offset = self._section_limits[section]['start']
                    entity["startOffset"] = entity["startOffset"] - section_offset
                    entity["endOffset"] = entity["endOffset"] - section_offset
                    break
        return

    def is_entity_in_section(self, entity, section):
        """
        For a given entity and a section, determines whether or not the entity belong to the section.
        """
        is_after_start = entity['startOffset'] >= self._section_limits[section]['start']
        is_before_end = entity['startOffset'] <= self._section_limits[section]['end']
        return is_after_start and is_before_end

    @classmethod
    def compute_sections_limits(cls, article, sections) -> dict:

        sections_limits = {}
        limit_previous_sec = -len(SECTION_SEPARATOR)
        for i in sections:
            section_start = limit_previous_sec + len(SECTION_SEPARATOR)
            sections_limits[i] = {
                'start': section_start,
                'end': len(article[i]) + section_start
            }
            limit_previous_sec = len(article[i]) + section_start
        return sections_limits
