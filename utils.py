
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

    if not(os.path.exists(LOGS_DIR)):
        logging.info('%s folder does not exist', LOGS_DIR)
        os.makedirs(LOGS_DIR)
        logging.info('%s folder created.', LOGS_DIR)

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