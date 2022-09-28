import json
from datetime import datetime

import boto3
import fr_core_news_md
from flask import request, Response
from flask_restplus import Resource, fields
from text_toolkit.entity_names import name_is_too_small

from app.config.definitions import OUTPUT_QUEUE_URL
from app.config.field_names import named_entities, id, title
from app.config.logging import logger
from app.config.restplus import api
from app.helpers.body_loader import Body_Loader
from app.helpers.section_handler import SectionHandler

ns = api.namespace('NamedEntityExtractor', description='Named Entity Extraction Service')
# entry format specification ( no strict verification was added on the swagger UI )
raw_text_entry = \
    api.model('entry_text', {
        'docID': fields.String(description='text to analyse', required=True,
                               example='000f57d6c10cb64d8b1fb26dab7731a9'),
        'bodyKey': fields.String(description='bodyKey', required=True,
                                 example='s3://s3-dev-document-body/000f57d6c10cb64d8b1fb26dab7731a9'),
        'title': fields.String(description='Article Title', required=True,
                               example="Ardèche Vernosc-lès-Annonay : la maison Sève peine à écouler ses produits")
    })

# nlp should only load once if declared here
nlp = fr_core_news_md.load()


@ns.route('/')
@api.expect(raw_text_entry, validate=False)
class OpsDiscriminantCalculator(Resource):
    def post(self):
        """
        Extracts named entities from the provided entry text
        """
        sqs = boto3.client('sqs', region_name='eu-west-3')
        entry_time = datetime.today()
        message = request.json
        logger.info("Received document {} for treatment ".format(message[id]))
        try:
            text = Body_Loader(message).load_article_body()
            message_with_sections = {
                "title": message[title],
                "text": text
            }
            section_handler = SectionHandler(message_with_sections, sections=('text', 'title'))

            ner_results = [
                {
                    "text": ent.text,
                    "label": ent.label_,
                    "startOffset": ent.start_char,
                    "endOffset": ent.end_char,
                    "source": "ner",
                    "articleSection": "text"
                } for ent in nlp(section_handler.full_text).ents if not name_is_too_small(ent.text)]

            section_handler.attribute_Section_To_Ner(ner_results)
            message[named_entities] = ner_results
            json_output = json.dumps(message, ensure_ascii=False)

            sqs.send_message(
                QueueUrl=OUTPUT_QUEUE_URL,
                MessageBody=json_output,
                MessageAttributes={"entry_time": {"DataType": "String", "StringValue": str(entry_time)}}
            )
            logger.info("Document {} with nlp result was sent to output queue".format(message[id]))
            response = Response("article treated and sent to output queue, id : {} ".format(message[id]), status=200)
        except Exception as ex:
            logger.info("Document {} could not be treated".format(message[id]))
            response = Response(ex.__str__(), status=500)

        return response
