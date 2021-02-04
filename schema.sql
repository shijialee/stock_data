CREATE TABLE IF NOT EXISTS symbol (
    "symbol" text not null,
    "market" text not NULL
);
CREATE UNIQUE INDEX symbol_market_symbol_idx ON symbol(symbol, market);

CREATE TABLE IF NOT EXISTS "history" (
  "symbol" TEXT NOT NULL,
  "date" DATE NOT NULL,
  "open" REAL,
  "high" REAL,
  "low" REAL,
  "close" REAL,
  "volume" INTEGER,
  "ma30" REAL
);
CREATE UNIQUE INDEX history_symbol_date_idx ON history(symbol, date);

CREATE TABLE IF NOT EXISTS "history_tmp" (
  "symbol" TEXT NOT NULL,
  "date" DATE NOT NULL,
  "open" REAL,
  "high" REAL,
  "low" REAL,
  "close" REAL,
  "volume" INTEGER,
  "ma30" REAL
);

CREATE TABLE IF NOT EXISTS "moving_average" (
"symbol" TEXT,
  "date" TEXT,
  "close" REAL,
  "ma30" REAL
);
CREATE UNIQUE INDEX moving_average_symbol_date_idx ON moving_average(symbol, date);

CREATE TABLE IF NOT EXISTS "moving_average_tmp" (
"symbol" TEXT,
  "date" TEXT,
  "close" REAL,
  "ma30" REAL
);

CREATE TABLE IF NOT EXISTS "breakout" (
  "symbol" TEXT NOT NULL,
  "date" DATE NOT NULL,
  "ma30" REAL,
  "close" REAL,
  "big_base" BOOLEAN,
  "rs_uptrend" BOOLEAN,
  "ma_bounced_from_bottom" BOOLEAN,
  "max_ma_one_year_ago" BOOLEAN
);
CREATE UNIQUE INDEX breakout_symbol_date_idx ON breakout(symbol, date);

CREATE TABLE IF NOT EXISTS "breakout_backtest_result" (
  "symbol" TEXT NOT NULL,
  "date" DATE NOT NULL,
  "ma30_ratio" REAL,
  "close_ratio" REAL,
  "year" INTEGER,
  "type" TEXT
);
