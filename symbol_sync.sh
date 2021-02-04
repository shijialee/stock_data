#!/bin/sh

CSV_FILE='/tmp/symbols.csv'
SYMBOL_DB_TABLE='symbol'
SQLITE_DB_FILE='stocks.sqlite'
IMPORT_SQL_FILE='/tmp/import_symbols.sql'
#SYMBOL_URL='ftp://ftp.nasdaqtrader.com/symboldirectory/nasdaqtraded.txt'
SYMBOL_URL='http://www.nasdaqtrader.com/dynamic/SymDir/nasdaqtraded.txt'

tee $IMPORT_SQL_FILE >/dev/null << EOF
DROP TABLE ${SYMBOL_DB_TABLE};
CREATE TABLE ${SYMBOL_DB_TABLE} (symbol text not null, market text not null);
CREATE UNIQUE INDEX market_symbol_idx ON ${SYMBOL_DB_TABLE}(name, market);
.separator ,
.import ${CSV_FILE} ${SYMBOL_DB_TABLE}
EOF

# skip ETF for column 5. skip test issue for colum 7
echo -n "Fetching and Importing symbols..."
curl -s $SYMBOL_URL |
perl -F'\|' -anle 'next if $.==1; next if $F[5] eq "Y"; next if $F[7] eq "Y"; print "$F[1],$F[3]" if $F[3]' > $CSV_FILE &&
sqlite3 $SQLITE_DB_FILE < $IMPORT_SQL_FILE 2>/dev/null
