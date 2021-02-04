## Goal

Get historical data to do backtesting.

## Prepare

* refresh nasdaq / nyse symbols, run this periodically to get latest symbols.
  * `source symbol_sync.sh`
* create required sqlite tables
  * `sqlite3 stocks.sqlite < schema.sql`

## Run

* setup bash env STOCK_LOG_LEVEL for log level
  * for example: `export STOCK_LOG_LEVEL=DEBUG`
* get history since 2021-01-01
  * `python history.py --date 2021-01-01 > /tmp/history.log 2>&1`
* generate moving average for last 300 days - need at least 150 working days data
  * `python moving_average.py 300`
