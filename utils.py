
"""Code Utilities."""

# External resources
import os
import logging
import glob
import fitz
import requests
from constants import (TEMP_DIR, LOGS_DIR,
                       NANONETS_URL)

# Constants
CWD = os.getcwd()

# Utilities

def ensure_logs_directory():
    """Create/Confirm logs directory"""
    if not(os.path.exists(LOGS_DIR)):
        os.makedirs(LOGS_DIR)
        

def house_keeping():
    """Create Temp folder if not exists. Otherwise empty it. Also create LOGS folder"""
    if os.path.exists(TEMP_DIR):
        logging.info('%s folder exists', TEMP_DIR)
        contents = glob.glob(f'{CWD}/{TEMP_DIR}/*')
        logging.debug('Contents found: %s', contents)
        quantity = 0
        for content in contents:
            logging.debug('removing file %s', content)
            os.remove(content)
            quantity += 1
        logging.info('%s contents deleted', quantity)

    else:
        logging.info('%s folder does not exist', TEMP_DIR)
        os.makedirs(TEMP_DIR)
        logging.info('%s folder created.', TEMP_DIR)

    logging.info('house_keeping() function executed successfully.')

def pdf_to_images(pdf_file_path):
    """Convert pdf to images for image hashing. Also Generate a hash list."""
    pdf = fitz.open(pdf_file_path)
    pdf_file_name = pdf_file_path.split('/')[-1].split('.')[0]
    logging.debug('UTILS.PY: pdf opened: %s', pdf_file_name)
    page_count = pdf.pageCount
    logging.info('UTILS.PY: %s has %s pages.', pdf_file_name, page_count)
    
    for page_number in range(page_count):
        page = pdf.load_page(page_number)
        pix = page.get_pixmap()
        output = TEMP_DIR + '/' + pdf_file_name.strip().replace(' ','_') + '_' +str(page.number+1) + '.jpg'
        logging.debug('UTILS.PY: image generated: %s', output)
        pix.save(output)
    return page_count

def get_nanonets_response(input_image):
    """Get Nanonet response & save for every image."""
    image_name=input_image.split('/')[-1]
    print(f'Processing Image: {image_name}')
    logging.info('Processing Image: %s', image_name)
    data = {'file': open(input_image, 'rb')}
    print('     Pinging for response')
    logging.info('     Pinging for response')
    response = requests.post(NANONETS_URL, auth=requests.auth.HTTPBasicAuth('O4L1LLEkCbEGfQmDr7-1fTKM2hAZTez3', ''), files=data)
    print('     Response received.')
    logging.info('     Response received.')
    return response.json()

def has_increment (text):
    try:
        int(text)
        return True
    except ValueError:
        return False

def find_increment(key_text, dict_instance):
    """split key text into str & int"""
    int_part = key_text.split('_')[-1]
    partitioned_key = key_text.rpartition('_')

    if has_increment(int_part):
        new_increment = int(partitioned_key[-1]) + 1
        new_key = partitioned_key[0] + '_' +str(new_increment)
        if new_key in dict_instance.keys():
            return find_increment(key_text=new_key, dict_instance=dict_instance)
        else:
            print(f'New increment identified: {new_key}')
            return new_key
    else:
        key_text = key_text + '_' + str(1)
        if key_text in dict_instance.keys():
            return find_increment(key_text, dict_instance)
        return key_text

def clean_br_json(raw_br_json):
    """Return clean BR json"""

    br_clean = {}

    for iterator, key in enumerate(raw_br_json.keys()):
        page_fields = raw_br_json[key]
        page_results = page_fields['result']
        for result in page_results:
            for prediction in result['prediction']:
                if 'BR' in prediction['label']:
                    br_clean[prediction['label']] = prediction['ocr_text']
    return br_clean

def clean_nn_json(raw_nn_json):
    """Return Clean NNAR-1 & NNAC-1 json"""

    clean_nn = {}

    for iterator, key in enumerate(raw_nn_json.keys()):
        page_fields = raw_nn_json[key]
        page_results = page_fields['result']
        for result in page_results:
            page_array = {}
            for prediction in result['prediction']:
                if 'NN' in prediction['label']:
                    field_key = prediction['label']
                    if field_key in page_array.keys():
                        field_key = find_increment(field_key, page_array)
                    page_array[field_key] = prediction['ocr_text']

                if prediction['label'] == 'table':
                    table_array = {}
                    for cell in prediction['cells']:
                        field_key = cell['label']
                        if field_key in table_array.keys():
                            field_key = find_increment(field_key, table_array)
                        table_array[field_key] = cell['text']
                    field_key = prediction['label']
                    if field_key in page_array.keys():
                        field_key = find_increment(field_key, page_array)
                    page_array[field_key] = table_array
        clean_nn[iterator] = page_array

    return clean_nn