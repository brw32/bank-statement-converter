import pandas as pd
from datetime import datetime

# Bank format definitions
BANK_FORMATS = {
    'chase': {
        'date': 'Posting Date',
        'description': 'Description',
        'amount': 'Amount'
    },
    'bofa': {
        'date': 'Date',
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

def convert_bank_to_qbo(input_file, output_file='qbo_ready.csv'):
    """
    Convert bank statement CSV to QuickBooks-ready format
    
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
    
    # Read file
    df = pd.read_csv(input_file)
    print(f"Loaded {len(df)} transactions")
    
    # Detect bank format
    bank_type, format_map = detect_bank_format(df)
    
    # Map to standard columns
    qbo_df = pd.DataFrame({
        'Date': df[format_map['date']],
        'Description': df[format_map['description']],
        'Amount': df[format_map['amount']]
    })
    
    # Clean and format
    qbo_df['Description'] = qbo_df['Description'].str.strip()
    qbo_df['Amount'] = pd.to_numeric(qbo_df['Amount'], errors='coerce')
    
    # Sort by date
    qbo_df['Date'] = pd.to_datetime(qbo_df['Date'])
    qbo_df = qbo_df.sort_values('Date')
    qbo_df['Date'] = qbo_df['Date'].dt.strftime('%m/%d/%Y')
    
    # Remove rows with missing data
    qbo_df = qbo_df.dropna()
    
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
    print("Bank Statement to QuickBooks Converter")
    print("=" * 40)
    
    result = convert_bank_to_qbo('sample_input.csv', 'qbo_ready.csv')
    print(f"\nConverted {len(result)} transactions successfully!")
