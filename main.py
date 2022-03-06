"""Execute Code."""

# External resources
import logging
from datetime import datetime
import os
from constants import TEMP_DIR, NANONETS_URL, LOGS_DIR, PDF_FILE
from utils import house_keeping, pdf_to_images, get_nanonets_response
import warnings
warnings.filterwarnings('ignore')

# Constants
DATETIME_STRING = datetime.now().strftime("%Y_%m_%d-%H_%M")
LOGS_FILE_NAME = f'{LOGS_DIR}/ALL-LOGS-' + DATETIME_STRING + '.log'

# logger
logging.basicConfig(filename=LOGS_FILE_NAME,
                    level=logging.DEBUG)
logging.info('MAIN.PY: LOGGER INITIALIZED at %s',  DATETIME_STRING)

# Code
# Create/Empty Temp folder & create LOGS folder
house_keeping()

# Generate images
page_count = pdf_to_images(pdf_file_path=PDF_FILE)

# Get Nanonets response
RESPONSES = []
images = os.listdir(TEMP_DIR)
for page in range(0, page_count):
    input_image = images[page]
    RESPONSES.append(get_nanonets_response(input_image=input_image))