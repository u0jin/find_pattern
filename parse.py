import pandas as pd

# Load the raw transaction data
raw_data = pd.read_csv('other.Transaction_bc1q5tvvnwzhd96ep299vfcarq0vrkuudqu8wtpyny.csv')

# Perform data cleaning and preprocessing
# ... (perform necessary data cleaning procedures here)

# Extract relevant columns for the network graph
preprocessed_data = raw_data[['sending_wallet', 'receiving_wallet', 'date_sent', 'transaction_amount']]

# Save the preprocessed data as CSV
preprocessed_data.to_csv('preprocessed_data.csv', index=False)
