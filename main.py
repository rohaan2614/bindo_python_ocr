"""Execute Code."""

# External resources
import logging
from datetime import datetime
import os
import argparse
import json
from constants import TEMP_DIR, LOGS_DIR
from utils import (house_keeping, pdf_to_images, 
                   get_nanonets_response, ensure_logs_directory,
                   clean_br_json, clean_nn_json)
import warnings
warnings.filterwarnings('ignore')

# Constants
DATETIME_STRING = datetime.now().strftime("%Y_%m_%d-%H_%M")
LOGS_FILE_NAME = f'{LOGS_DIR}/ALL-LOGS-' + DATETIME_STRING + '.log'
RESPONSES = {}

# logs directory
ensure_logs_directory()

# logger
logging.basicConfig(filename=LOGS_FILE_NAME,
                    level=logging.DEBUG)
logging.info('MAIN.PY: LOGGER INITIALIZED at %s',  DATETIME_STRING)

# Create/Empty Temp folder
house_keeping()

# read arguments
PARSER = argparse.ArgumentParser(description= 'example: --in-file="./Samples/Better_World_Development.pdf" --out-file="nar-output.json"')
PARSER.add_argument('--in-file', help = 'in document path')
PARSER.add_argument('--out-file', help = 'output json path')
arguments = PARSER.parse_args()

# Generate images
page_count = pdf_to_images(pdf_file_path=arguments.in_file)

# Get Nanonets response
images = os.listdir(TEMP_DIR)
images.sort()
for page in range(0, page_count):
    input_image = f'{TEMP_DIR}/{images[page]}'
    RESPONSES[str(page)] = get_nanonets_response(input_image=input_image)

if 'br_' in arguments.in_file.lower():
    RESPONSES = clean_br_json(RESPONSES)
elif 'nnar_' in arguments.in_file.lower() or 'nnac' in arguments.in_file.lower():
    RESPONSES = clean_nn_json(RESPONSES)

# Write output
with open(arguments.out_file, "w") as outfile:
    json.dump(RESPONSES, outfile)
    logging.info('Data dumped to output Json file.')
    print('Ouput Json saved.')
