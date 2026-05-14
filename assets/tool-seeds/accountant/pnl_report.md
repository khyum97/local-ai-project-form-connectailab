<!-- version: pnl_report_v1 -->
# pnl_report - business P&L markdown report

Reads a transaction CSV and summarizes revenue, expense, fees, and net profit.

## Config
- `CSV_FILE`: trade CSV path
- `FEE_COLUMN`: optional fee column name, default `fee`
- `OUTPUT_FILE`: optional markdown output path

Expected columns: `category`, `type`, `amount`, optional `fee`.
`type` can be `revenue`, `income`, `expense`, `cost`, or `fee`.
