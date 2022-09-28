import os


if "OUTPUT_QUEUE_URL" in os.environ:
    OUTPUT_QUEUE_URL = os.environ["OUTPUT_QUEUE_URL"]
else:
    OUTPUT_QUEUE_URL = None

SECTION_SEPARATOR = 'SEP'