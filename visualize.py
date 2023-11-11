import pandas as pd
import matplotlib.pyplot as plt
import argparse


def extract_and_process(filename, target_year, target_month):
    expenses_df = pd.read_csv(filename, index_col=None)
    filtered_expenses = filter_expenses_by_month(expenses_df, target_year, target_month)
    category_sum_df = filtered_expenses.groupby('Category')['Amount'].sum().reset_index()
    category_sum_df['Amount'] = category_sum_df['Amount'].round().astype(int)
    category_sum_df.to_csv('temp.csv', index=False)
    # Sort the DataFrame by 'Amount' column in descending order
    category_sum_df = category_sum_df.sort_values(by='Amount', ascending=False)

    # Create a bar chart
    plt.figure(figsize=(10, 6))
    bars = plt.bar(category_sum_df['Category'], category_sum_df['Amount'])
    plt.xlabel('Category')
    plt.ylabel('Total Amount (Rounded)')
    plt.title(f'Category-wise Expense Sum for {target_month}/{target_year}')
    plt.xticks(rotation=45, ha='right')  # Rotate the x-axis labels for better visibility
    
    # Add numbers above each bar
    for bar in bars:
        height = bar.get_height()
        plt.annotate('{}'.format(height),
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 3),  # 3 points vertical offset
                     textcoords="offset points",
                     ha='center', va='bottom')

    # Display the chart
    plt.tight_layout()
    plt.show()


def custom_date_parser(date_string):
    # Attempt to parse the date using the first format
    try:
        return pd.to_datetime(date_string, format='%B %d, %Y')
    except ValueError:
        # If parsing with the first format fails, try the second format
        parts = date_string.split(" → ")
        if len(parts) == 2:
            return pd.to_datetime(parts[0], format='%B %d, %Y')
        else:
            # Handle any other format errors by returning NaT
            return pd.NaT

def filter_expenses_by_month(df, target_year, target_month):
    df['Date'] = df['Date'].apply(custom_date_parser)
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    filtered_df = df[(df['Year'] == target_year) & (df['Month'] == target_month)]
    return filtered_df

def main():
    parser = argparse.ArgumentParser(description='Process expenses for a specific month and year.')
    parser.add_argument('filename', type=str, help='CSV file containing expenses data')
    parser.add_argument('year', type=int, help='Year to filter on')
    parser.add_argument('month', type=int, help='Month (1-12) to filter on')

    args = parser.parse_args()
    filename = args.filename
    target_year = args.year
    target_month = args.month

    print(f"Processing expenses for {target_month}/{target_year}")
    extract_and_process(filename, target_year, target_month)

if __name__ == "__main__":
    main()