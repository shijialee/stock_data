import pandas as pd
import sys
from datetime import timedelta, datetime
from utils import get_logger, get_symbols, get_db_connection

window = 150
history_tbl = 'history'
moving_average_tbl = 'moving_average'
moving_average_tmp_tbl = 'moving_average_tmp'
conn = get_db_connection()
logger = get_logger(__name__)


# optimize so we don't rebuild MA for all history data
def get_where_date():
    if len(sys.argv) == 1:
        return ''

    date = datetime.now() - timedelta(days=int(sys.argv[1]))
    start_date = date.strftime('%Y-%m-%d')
    return f'and date > "{start_date}"'


def cli():
    where_date = get_where_date()

    symbols = get_symbols()
    for symbol in symbols:
        logger.debug(f"{symbol}")
        data = pd.read_sql_query(
            f'select date, close from history where symbol = "{symbol}" {where_date} order by date',
            conn,
            index_col='date'
        )
        # skip if not enough data
        if len(data.index) < window:
            continue

        data['ma30'] = data['close'].rolling(window).mean()
        data = data.round({'ma30': 2})
        data.reset_index(inplace=True)
        data.insert(0, 'symbol', symbol)
        data.to_sql(moving_average_tmp_tbl, conn, if_exists='append', index=False)

    # insert without worrying dupe
    logger.info(f"MA calculated. loading to table now")
    with conn:
        insert_sql = f'INSERT OR IGNORE INTO {moving_average_tbl} SELECT * FROM {moving_average_tmp_tbl}'
        delete_sql = f'DELETE FROM {moving_average_tmp_tbl}'
        conn.execute(insert_sql)
        conn.execute(delete_sql)
    # update history table with ma30
    # sql = ('UPDATE history h JOIN moving_average ma'
    #        ' ON ma.symbol = h.symbol AND ma.date = h.date'
    #        ' SET h.ma30 = ma.ma30'
    #        ' WHERE h.ma30 IS NOT NULL AND ma.ma30 IS NOT NULL'
    # )
    # conn.execute(sql)


if __name__ == '__main__':
    cli()
