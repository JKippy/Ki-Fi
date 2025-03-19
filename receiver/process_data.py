import pandas as pd
from datetime import datetime
import os

def process_csv_to_excel(csv_path, excel_path):
    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    # Convert timestamp to datetime
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')
    
    # Create Excel writer
    with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
        # Write the dataframe to Excel
        df.to_excel(writer, sheet_name='Messages', index=False)
        
        # Get the workbook and worksheet objects
        workbook = writer.book
        worksheet = writer.sheets['Messages']
        
        # Define formats
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#4B0082',
            'font_color': 'white',
            'border': 1
        })
        
        cell_format = workbook.add_format({
            'border': 1,
            'text_wrap': True
        })
        
        # Format the header
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
        
        # Set column widths
        worksheet.set_column('A:A', 20)  # Timestamp column
        worksheet.set_column('B:B', 50)  # Message column
        
        # Format all cells
        for row in range(1, len(df) + 1):
            for col in range(len(df.columns)):
                worksheet.write(row, col, df.iloc[row-1, col], cell_format)

def main():
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define input and output paths
    csv_path = os.path.join(current_dir, 'messages.csv')
    excel_path = os.path.join(current_dir, 'messages.xlsx')
    
    try:
        process_csv_to_excel(csv_path, excel_path)
        print(f"Successfully converted {csv_path} to {excel_path}")
    except Exception as e:
        print(f"Error processing file: {str(e)}")

if __name__ == "__main__":
    main() 