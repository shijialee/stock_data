import yfinance as yf
import argparse
from datetime import timedelta, datetime
from utils import get_logger, get_symbols, get_db_connection


history_tbl = 'history'
history_tmp_tbl = 'history_tmp'
conn = get_db_connection()
logger = get_logger(__name__)


def fetch_and_insert_history(symbol, start_date):
    ticker = yf.Ticker(symbol)
    # if specify end=end_date, end_date is not inclusive
    history = ticker.history(start=start_date)
    if history.empty:
        logger.info(f'{symbol} no data')
        return None

    # convert index to column
    history.reset_index(inplace=True)
    # format column
    history.columns = history.columns.str.lower().str.replace(' ', '_')
    # round to last two decimal digits
    history = history.round({'open': 2, 'high': 2, 'low': 2, 'close': 2})
    # drop unnecessary columns
    history.drop(columns=['dividends', 'stock_splits'], inplace=True)

    # convert to date
    history['date'] = history['date'].dt.date
    # add symbol as column
    history.insert(0, 'symbol', symbol)

    history.to_sql(history_tmp_tbl, conn, if_exists='append', index=False)


def get_start_date():
    monday = datetime.now() - timedelta(days=0)
    default_start_weekly = monday.strftime('%Y-%m-%d')

    # get last X years historical data
    init_date = datetime.now() - timedelta(days=365*20)
    default_start_init = init_date.strftime('%Y-%m-%d')

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--init",
        nargs='?',
        const=default_start_init,
        help="init the historical db")
    group.add_argument(
        "--weekly",
        nargs='?',
        const=default_start_weekly,
        help="append this week historical data to db")
    group.add_argument(
        "--date",
        help="specify a start date(Y-m-d) to fetch history")
    args = parser.parse_args()

    if args.date:
        # validate input
        datetime.strptime(args.date, "%Y-%m-%d")
        return args.date
    if args.weekly:
        return default_start_weekly
    if args.init:
        return default_start_init
    raise Exception('no valid arg')


def cli():
    start_date = get_start_date()
    symbols = get_symbols()
    # XXX also get Dow Jones Industrial Average
    symbols.append('DJI')

    for symbol in symbols:
        logger.debug(f"{symbol}")
        fetch_and_insert_history(symbol, start_date)

    logger.info(f"all symbols fetched. loading to table now")
    # insert without worrying dupe
    with conn:
        insert_sql = f'INSERT OR IGNORE INTO {history_tbl} SELECT * FROM {history_tmp_tbl}'
        delete_sql = f'DELETE FROM {history_tmp_tbl}'
        conn.execute(insert_sql)
        conn.execute(delete_sql)


if __name__ == '__main__':
    cli()
