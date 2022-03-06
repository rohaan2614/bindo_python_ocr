"""Constants used by the code."""

import configparser

CONFIG = configparser.ConfigParser()

CONFIG.read_file(open('config.cfg', encoding='UTF-8'))

TEMP_DIR = CONFIG.get('DIRECTORIES', 'TEMP')
LOGS_DIR = CONFIG.get('DIRECTORIES', 'LOGS')
NANONETS_URL = CONFIG.get('NANONETS', 'URL')

PDF_FILE = CONFIG.get('DOCUMENTS', 'NAR')