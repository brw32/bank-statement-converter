# Bank Statement to QuickBooks Converter

A Python tool that converts bank statement CSV files into QuickBooks Online-ready format. Saves hours of manual data entry for bookkeepers and small business owners.

## 🎯 Problem Solved

Manually entering bank transactions into QuickBooks is tedious and error-prone. Most banks export CSVs, but the format doesn't match what QuickBooks expects. This tool bridges that gap.

## ✨ Features

- 📊 Converts bank CSV exports to QuickBooks-compatible format
- 🏦 Auto-detects bank format (Chase, Bank of America, Wells Fargo, generic)
- ✅ Cleans and validates transaction data
- 📅 Proper date formatting for QBO import
- 💰 Handles debits/credits correctly
- 📈 Provides transaction summary statistics

## 🚀 Quick Start

### Installation
```bash
pip install pandas
```

### Usage
```bash
python converter.py
```

The script will:
1. Read `sample_input.csv`
2. Auto-detect the bank format
3. Convert to QuickBooks format
4. Save as `qbo_ready.csv`

### Custom Files
```python
from converter import convert_bank_to_qbo

# Convert your own bank statement
result = convert_bank_to_qbo('my_bank_statement.csv', 'output.csv')
```

## 📋 Input Format

Your bank CSV should have these columns (names may vary):
- **Date** - Transaction date
- **Description** - Transaction description
- **Amount** - Transaction amount (negative for debits, positive for credits)

## 💼 Use Case

**Before:** 
- Export bank statement CSV
- Manually enter 200+ transactions into QuickBooks
- Fix formatting errors
- Time: 3-4 hours

**After:**
- Export bank statement CSV
- Run through converter
- Import into QuickBooks
- Time: 5 minutes

## 🏦 Supported Banks

- Chase Bank
- Bank of America
- Wells Fargo
- Any bank with standard CSV format (Date, Description, Amount)

## 🔧 Tech Stack

- **Python 3.8+**
- **Pandas** - Data processing and manipulation

## 📊 Example Output
```
Bank Statement to QuickBooks Converter
========================================
Reading: sample_input.csv
Loaded 7 transactions
Bank format detected: BOFA
Saved to: qbo_ready.csv

Summary:
   Transactions: 7
   Credits: $4,350.00
   Debits: $-344.79
   Net: $4,005.21

Ready to import to QuickBooks Online
```



## ✅ Tested with Real Data

This tool has been tested with actual Bank of America statements containing:
- Multiple header rows
- 4-column format (Date, Description, Amount, Running Balance)
- Formatted amounts with commas (e.g., "1,234.56")
- 60+ transactions

**Real-world test results:**
- Input: 67-row BofA CSV export
- Output: 66 clean QuickBooks-ready transactions
- Processing time: <1 second

## 👨‍💻 Author

**Brian Wittig** - Python Developer & QuickBooks ProAdvisor

- 🌐 Website: [brianwittig.com](https://brianwittig.com)
- 📧 Email: brian@brianwittig.com
- 💼 LinkedIn: [linkedin.com/in/brianwittig](https://linkedin.com/in/brianwittig)
- 🏢 Owner, Brian Wittig & Associates, LLC (22+ bookkeeping clients)

## 📄 License

MIT License - Free to use and modify

## 🤝 Contributing

This is a portfolio project demonstrating Python automation for accounting workflows. Suggestions and improvements are welcome!

---

**Built with real-world bookkeeping experience | Tested on actual client data**
