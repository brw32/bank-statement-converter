import pandas as pd
from datetime import datetime

# Bank format definitions
BANK_FORMATS = {
    'bofa_detailed': {
        'date': 'Date',
        'description': 'Description',
        'amount': 'Amount'
    },
    'chase': {
        'date': 'Posting Date',
        'description': 'Description',
        'amount': 'Amount'
    },
    'wells': {
        'date': 'Date',
        'description': 'Description',
        'amount': 'Amount'
    },
    'generic': {
        'date': 'Date',
        'description': 'Description',
        'amount': 'Amount'
    }
}

def detect_bank_format(df):
    """
    Auto-detect which bank format this CSV is
    """
    columns = [col.strip() for col in df.columns.tolist()]
    
    for bank, format_map in BANK_FORMATS.items():
        required_cols = list(format_map.values())
        if all(col in columns for col in required_cols):
            print(f"Bank format detected: {bank.upper()}")
            return bank, format_map
    
    print("Unknown format, using generic")
    return 'generic', BANK_FORMATS['generic']

def clean_amount(amount_str):
    """
    Clean amount string - remove commas, handle empty strings
    """
    if pd.isna(amount_str) or amount_str == '':
        return None
    
    # Remove commas and quotes
    cleaned = str(amount_str).replace(',', '').replace('"', '').strip()
    
    try:
        return float(cleaned)
    except:
        return None

def convert_bank_to_qbo(input_file, output_file='qbo_ready.csv'):
    """
    Convert bank statement CSV to QuickBooks-ready format
    
    Handles:
    - Multiple header rows (skips until it finds column headers)
    - Extra columns (like Running Balance)
    - Amounts with commas
    - Empty amount fields
    
    Parameters:
    -----------
    input_file : str
        Path to bank statement CSV file
    output_file : str
        Path for output QuickBooks-ready CSV
        
    Returns:
    --------
    DataFrame : The converted data
    """
    print(f"Reading: {input_file}")
    
    # Read file - skip rows until we find the header
    # Look for a row that contains "Date" and "Description" and "Amount"
    found_header = False
    skip_rows = 0
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if 'Date' in line and 'Description' in line and 'Amount' in line:
                skip_rows = i
                found_header = True
                break
    
    if not found_header:
        print("Warning: Could not find header row, assuming first row")
        skip_rows = 0
    
    # Read with correct header row
    df = pd.read_csv(input_file, skiprows=skip_rows)
    
    print(f"Loaded {len(df)} rows")
    
    # Detect bank format
    bank_type, format_map = detect_bank_format(df)
    
    # Map to standard columns (only keep what we need)
    qbo_df = pd.DataFrame({
        'Date': df[format_map['date']],
        'Description': df[format_map['description']],
        'Amount': df[format_map['amount']]
    })
    
    # Clean description
    qbo_df['Description'] = qbo_df['Description'].str.strip()
    
    # Clean and convert amounts
    qbo_df['Amount'] = qbo_df['Amount'].apply(clean_amount)
    
    # Remove rows with missing amounts or dates
    qbo_df = qbo_df.dropna(subset=['Amount', 'Date'])
    
    # Convert dates
    qbo_df['Date'] = pd.to_datetime(qbo_df['Date'])
    qbo_df = qbo_df.sort_values('Date')
    qbo_df['Date'] = qbo_df['Date'].dt.strftime('%m/%d/%Y')
    
    print(f"Valid transactions: {len(qbo_df)}")
    
    # Save
    qbo_df.to_csv(output_file, index=False)
    print(f"Saved to: {output_file}")
    
    # Summary
    credits = qbo_df[qbo_df['Amount'] > 0]['Amount'].sum()
    debits = qbo_df[qbo_df['Amount'] < 0]['Amount'].sum()
    print(f"\nSummary:")
    print(f"   Transactions: {len(qbo_df)}")
    print(f"   Credits: ${credits:,.2f}")
    print(f"   Debits: ${debits:,.2f}")
    print(f"   Net: ${(credits + debits):,.2f}")
    print(f"\nReady to import to QuickBooks Online")
    
    return qbo_df

if __name__ == "__main__":
    # Example usage
    print("Bank Statement to QuickBooks Converter v2")
    print("=" * 40)
    
    result = convert_bank_to_qbo('sample_input.csv', 'qbo_ready.csv')
    print(f"\nConverted {len(result)} transactions successfully!")
