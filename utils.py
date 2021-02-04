import logging
import sqlite3
import os
import sys


def get_db_connection():
    history_db_file = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'stocks.sqlite'
    )
    conn = sqlite3.connect(history_db_file)
    conn.row_factory = sqlite3.Row
    return conn


def get_symbols():
    return ['AAXN', 'RUN', 'MSFT', 'BABA', 'GME', 'SHOP', 'CGEN', 'MGI', 'CYH', 'BDR', 'CNSL', 'JD', 'NVDA', 'GRWG', 'NTZ']
    markets = ('Q', 'N')
    conn = get_db_connection()
    symbols = conn.execute('SELECT symbol FROM symbol WHERE market IN (?,?) order by symbol', markets).fetchall()
    if len(symbols) == 0:
        raise Exception('no symbols')
    return [item[0] for item in symbols if item[0].isalpha()]


def get_logger(name):
    logger = logging.getLogger(name)
    log_level = os.environ.get('STOCK_LOG_LEVEL', '').upper()
    if log_level:
        logger.setLevel(log_level)

        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(
            logging.Formatter(
                fmt="%(levelname)s [%(asctime)s] %(name)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        logger.addHandler(handler)

    return logger
