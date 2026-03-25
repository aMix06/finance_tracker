# Finance Tracker

This program takes a raw CSV Revolut bank statement, uses a local LLM 
to categorize each expense, and summarizes personal finances through 
calculations and visualizations.

## Features
- Weekly and monthly expense breakdowns
- Automatic expense categorization using a local LLM (Ollama)
- Spending visualizations by category
- Key statistics such as highest spending day, biggest expense, 
  and most frequent category

## Technologies Used
- Python 3.12
- pandas, matplotlib
- Ollama (local LLM — deepseek-r1:8b)

## Requirements
- Python 3.x installed
- Ollama installed and running locally
- A Revolut bank statement exported as a CSV file

## How to Run
1. Clone this repository
2. Install dependencies: `pip install pandas matplotlib ollama`
3. Export your Revolut bank statement as a CSV file and place 
   it in the project folder
4. Update the `file_path` variable in `bank_statement_handling.py` 
   to match your filename
5. Run: `python bank_statement_handling.py`

## Roadmap
- Interactive dashboard with drag and drop CSV upload
- PDF summary report generation
- Multi-month comparison
- Support for other bank CSV formats

## Notes
- Expense categories are cached locally in `categories.json` 
  to avoid repeated LLM calls
- Currently supports Revolut CSV format only