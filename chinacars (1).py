# -*- coding: utf-8 -*-
"""ChinaCars

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xflJo1gYQ5p15Nx_2L_G2noR2MMwgdcB
"""

# prompt: Using the file path /content/760k-Car-Owners-Nationwide-China-csv-2020.csv please create a code to read  and detect language and translate the column headers to English and save as a new csv

!pip install googletrans==4.0.0-rc1
!pip install langdetect

import pandas as pd
from googletrans import Translator
from langdetect import detect

def translate_headers(df):
    translator = Translator()
    new_headers = []
    for header in df.columns:
        try:
            detected_lang = detect(header)
            if detected_lang != 'en':
                translation = translator.translate(header, dest='en')
                new_headers.append(translation.text)
            else:
                new_headers.append(header)
        except:
            new_headers.append(header)
    return new_headers

# Read the CSV file
df = pd.read_csv('/content/760k-Car-Owners-Nationwide-China-csv-2020.csv ')

# Translate the headers
new_headers = translate_headers(df)
df.columns = new_headers

# Save the translated CSV
df.to_csv('/content/translated_car_owners.csv', index=False)

# prompt: using the file path /content/translated_car_owners.csv please generate a function to merge Province and city and address into one column Address dropping Province and city and address and drop duplicated lines

import pandas as pd

def merge_and_drop_duplicates(file_path):
    """
    Merges Province, City, and Address columns into one 'Address' column,
    drops the original columns, and removes duplicate rows.

    Args:
        file_path: The path to the CSV file.

    Returns:
        A new DataFrame with the merged address and dropped duplicates.
    """
    df = pd.read_csv(file_path)
    df['address'] = df['Province'].fillna('') + ', ' + df['City'].fillna('') + ', ' + df['address'].fillna('')
    df['address'] = df['address'].str.strip(', ')  # Remove leading/trailing commas and spaces
    df = df.drop(['Province', 'City'], axis=1)
    df = df.drop_duplicates()
    return df

# Example usage:
# Assuming your CSV file is in '/content/translated_car_owners.csv'
new_df = merge_and_drop_duplicates('/content/translated_car_owners.csv')
print(new_df)
# You can then save this new DataFrame to a new CSV file if needed:
# new_df.to_csv('merged_car_owners.csv', index=False)

import pandas as pd
import numpy as np
import re

# Define a function to validate email addresses
def is_valid_email(Mail):
    """
    Validates an email address using a regular expression.

    Args:
        email: The email address to validate.

    Returns:
        True if the email is valid, False otherwise.
    """
    # Handle missing or non-string values
    if pd.isnull(Mail) or not isinstance(Mail, str):
        return False

    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, Mail) is not None

def chunk_and_clean_data(file_path):
    """
    Chunks the data into 4 chunks, cleans the chunks, and creates a garbage file for removed data.

    Args:
        file_path: The path to the CSV file.
    """
    # Read the CSV file (suppressing DtypeWarning)
    df = pd.read_csv(file_path, low_memory=False)

    # Ensure the 'Mail' column exists, regardless of case sensitivity
    df.columns = df.columns.str.strip()  # Remove any leading/trailing spaces
    if 'Mail' not in df.columns:
        raise KeyError("The 'Mail' column is not present in the DataFrame.")

    # Drop specified columns
    df = df.drop(['Monthly salary', 'marriage', 'educate', 'color', 'Unnamed: 21'], axis=1)

    # Validate email addresses and create a column for invalid emails
    df['Valid Email'] = df['Mail'].apply(is_valid_email)

    # Define the columns to check for missing values
    required_columns = ['Frame number', 'ID card', 'Motor number', 'Mail']

    # Merge province, city, and address into one column
    df['full_address'] = df['Province'] + ', ' + df['City'] + ', ' + df['address']

    # Save dropped columns to garbage.csv
    dropped_columns = df[['Province', 'City', 'address']]
    dropped_columns.to_csv('garbage.csv', index=False)

    # Drop the original columns
    df.drop(columns=['Province', 'City', 'address'], inplace=True)

    # Split the data into 4 chunks
    chunks = np.array_split(df, 4)

    # Create a garbage DataFrame to store removed data
    garbage_df = pd.DataFrame(columns=df.columns)

    # Clean each chunk and collect garbage data
    cleaned_chunks = []
    for chunk in chunks:
        # Identify rows with missing or invalid data in the specified columns
        garbage_rows = chunk[chunk[required_columns].isnull().any(axis=1) | ~chunk['Valid Email']]

        # Append garbage rows to garbage_df
        garbage_df = pd.concat([garbage_df, garbage_rows])

        # Remove garbage rows from the chunk
        cleaned_chunk = chunk.dropna(subset=required_columns)
        cleaned_chunk = cleaned_chunk[cleaned_chunk['Valid Email']]

        # Drop the 'Valid Email' column as it's no longer needed
        cleaned_chunk = cleaned_chunk.drop(['Valid Email'], axis=1)

        # Append cleaned chunk to cleaned_chunks list
        cleaned_chunks.append(cleaned_chunk)

    # Save cleaned chunks to separate CSV files
    for i, cleaned_chunk in enumerate(cleaned_chunks):
        cleaned_chunk.to_csv(f'cleaned_chunk_{i+1}.csv', index=False)

    # Save garbage data to a separate CSV file
    garbage_df.to_csv('garbage_data.csv', index=False)

# Example usage
file_path = '/content/translated_car_owners (2).csv'
chunk_and_clean_data(file_path)

import pandas as pd
import numpy as np
import re

# Define a function to check for alphanumeric characters in email addresses
def has_alphanumeric(Mail):
    """
    Checks if the email address contains any alphanumeric characters.

    Args:
        Mail: The email address to check.

    Returns:
        True if the email contains alphanumeric characters, False otherwise.
    """
    # Handle missing or non-string values
    if pd.isnull(Mail) or not isinstance(Mail, str):
        return False

    # Check for alphanumeric characters
    return any(char.isalnum() for char in Mail)

def chunk_and_clean_data(file_path):
    """
    Chunks the data into 4 chunks, cleans the chunks, and creates a garbage file for removed data.

    Args:
        file_path: The path to the CSV file.
    """
    # Read the CSV file (suppressing DtypeWarning)
    df = pd.read_csv(file_path, low_memory=False)

    # Ensure the 'Mail' column exists, regardless of case sensitivity
    df.columns = df.columns.str.strip()  # Remove any leading/trailing spaces
    if 'Mail' not in df.columns:
        raise KeyError("The 'Mail' column is not present in the DataFrame.")

    # Drop specified columns
    df = df.drop(['Monthly salary', 'marriage', 'educate', 'color', 'Unnamed: 21'], axis=1)

    # Check for alphanumeric characters in email addresses and create a column for invalid emails
    df['Invalid Email'] = df['Mail'].apply(has_alphanumeric)

    # Define the columns to check for missing values
    required_columns = ['Frame number', 'ID card', 'Motor number', 'Mail']

    # Merge province, city, and address into one column
    df['full_address'] = df['Province'] + ', ' + df['City'] + ', ' + df['address']

    # Save dropped columns to garbage.csv
    dropped_columns = df[['Province', 'City', 'address']]
    dropped_columns.to_csv('garbage.csv', index=False)

    # Drop the original columns
    df.drop(columns=['Province', 'City', 'address'], inplace=True)

    # Split the data into 4 chunks
    chunks = np.array_split(df, 4)

    # Create a garbage DataFrame to store removed data
    garbage_df = pd.DataFrame(columns=df.columns)

    # Clean each chunk and collect garbage data
    cleaned_chunks = []
    for chunk in chunks:
        # Identify rows with missing or invalid data in the specified columns
        garbage_rows = chunk[chunk[required_columns].isnull().any(axis=1) | chunk['Invalid Email']]

        # Append garbage rows to garbage_df
        garbage_df = pd.concat([garbage_df, garbage_rows])

        # Remove garbage rows from the chunk
        cleaned_chunk = chunk.dropna(subset=required_columns)
        cleaned_chunk = cleaned_chunk[~cleaned_chunk['Invalid Email']]

        # Drop the 'Invalid Email' column as it's no longer needed
        cleaned_chunk = cleaned_chunk.drop(['Invalid Email'], axis=1)

        # Append cleaned chunk to cleaned_chunks list
        cleaned_chunks.append(cleaned_chunk)

    # Save cleaned chunks to separate CSV files
    for i, cleaned_chunk in enumerate(cleaned_chunks):
        cleaned_chunk.to_csv(f'cleaned_chunk_{i+1}.csv', index=False)

    # Save garbage data to a separate CSV file
    garbage_df.to_csv('garbage_data.csv', index=False)

# Example usage
file_path = '/content/translated_car_owners (2).csv'
chunk_and_clean_data(file_path)

import pandas as pd
import numpy as np
import re

# ... (The `has_alphanumeric` and `chunk_and_clean_data` functions from the previous response)

# Specify the file path
file_path = '/content/translated_car_owners (2).csv'

# Call the function to clean the data
cleaned_df = chunk_and_clean_data(file_path)

# Now you can work with the cleaned DataFrame (cleaned_df)
print(cleaned_df.head())  # Print the first few rows of the cleaned DataFrame
# ... (Perform other operations on the cleaned DataFrame as needed)

import pandas as pd
import numpy as np
import re

# Define a function to check for valid email addresses
def is_valid_email(email):
    """
    Checks if the email address is valid (contains alphanumeric characters and follows basic structure).

    Args:
        email: The email address to check.

    Returns:
        True if the email is valid, False otherwise.
    """
    # Handle missing or non-string values
    if pd.isnull(email) or not isinstance(email, str):
        return False

    # Basic regex for email validation (alphanumeric check included)
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def chunk_and_clean_data(file_path):
    """
    Chunks the data into 4 chunks, cleans the chunks, and creates a garbage file for removed data.

    Args:
        file_path: The path to the CSV file.
    """
    # Read the CSV file (suppressing DtypeWarning)
    df = pd.read_csv(file_path, low_memory=False)

    # Ensure the 'Mail' column exists, regardless of case sensitivity
    df.columns = df.columns.str.strip()  # Remove any leading/trailing spaces
    if 'Mail' not in df.columns:
        raise KeyError("The 'Mail' column is not present in the DataFrame.")
    # Drop specified columns if they exist
    columns_to_drop = ['Monthly salary', 'marriage', 'educate', 'color', 'Unnamed: 21']
    df = df.drop([col for col in columns_to_drop if col in df.columns], axis=1, errors='ignore')

    # Validate emails and create a column for invalid emails
    df['Invalid Email'] = df['Mail'].apply(lambda x: not is_valid_email(x))

    # Define the columns to check for missing values
    required_columns = ['Frame number', 'ID card', 'Motor number', 'Mail']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"The required column '{col}' is missing from the DataFrame.")

    # Merge province, city, and address into one column if they exist
    if all(col in df.columns for col in ['Province', 'City', 'address']):
        df['full_address'] = df['Province'].fillna('') + ', ' + df['City'].fillna('') + ', ' + df['address'].fillna('')

        # Save dropped columns to garbage.csv
        dropped_columns = df[['Province', 'City', 'address']]
        dropped_columns.to_csv('garbage.csv', index=False)

        # Drop the original columns
        df.drop(columns=['Province', 'City', 'address'], inplace=True)
    else:
        print("One or more of the columns 'Province', 'City', 'address' are missing.")

    # Split the data into 4 chunks
    chunks = np.array_split(df, 4)

    # Create a garbage DataFrame to store removed data
    garbage_df = pd.DataFrame(columns=df.columns)

    # Clean each chunk and collect garbage data
    cleaned_chunks = []
    for chunk in chunks:
        # Identify rows with missing or invalid data in the specified columns
        garbage_rows = chunk[chunk[required_columns].isnull().any(axis=1) | chunk['Invalid Email']]
        # Append garbage rows to garbage_df
        garbage_df = pd.concat([garbage_df, garbage_rows])
        # Remove garbage rows from the chunk
        cleaned_chunk = chunk.dropna(subset=required_columns)
        cleaned_chunk = cleaned_chunk[~cleaned_chunk['Invalid Email']]
        # Drop the 'Invalid Email' column as it's no longer needed
        cleaned_chunk = cleaned_chunk.drop(['Invalid Email'], axis=1)
        # Append cleaned chunk to cleaned_chunks list
        cleaned_chunks.append(cleaned_chunk)

    # Save cleaned chunks to separate CSV files
    for i, cleaned_chunk in enumerate(cleaned_chunks):
        cleaned_chunk.to_csv(f'cleaned_chunk_{i+1}.csv', index=False)

    # Save garbage data to a separate CSV file
    garbage_df.to_csv('garbage_data.csv', index=False)

# Example usage
file_path = '/content/translated_car_owners (2).csv'
chunk_and_clean_data(file_path)

import pandas as pd
import numpy as np
import re

# Define a function to check for valid email addresses
def is_valid_email(email):
    """
    Checks if the email address is valid (contains alphanumeric characters and follows basic structure).

    Args:
        email: The email address to check.

    Returns:
        True if the email is valid, False otherwise.
    """
    # Handle missing or non-string values
    if pd.isnull(email) or not isinstance(email, str):
        return False

    # Basic regex for email validation (alphanumeric check included)
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def chunk_and_clean_data(file_path):
    """
    Chunks the data into 4 chunks, cleans the chunks, and creates a garbage file for removed data.

    Args:
        file_path: The path to the CSV file.
    """
    # Read the CSV file (suppressing DtypeWarning)
    df = pd.read_csv(file_path, low_memory=False)

    # Ensure the 'Mail' column exists, regardless of case sensitivity
    df.columns = df.columns.str.strip()  # Remove any leading/trailing spaces
    if 'Mail' not in df.columns:
        raise KeyError("The 'Mail' column is not present in the DataFrame.")
    # Drop specified columns if they exist
    columns_to_drop = ['Monthly salary', 'marriage', 'educate', 'color', 'Unnamed: 21']
    df = df.drop([col for col in columns_to_drop if col in df.columns], axis=1, errors='ignore')

    # Validate emails and create a column for invalid emails
    df['Invalid Email'] = df['Mail'].apply(lambda x: not is_valid_email(x))

    # Define the columns to check for missing values
    required_columns = ['Frame number', 'ID card', 'Motor number', 'Mail']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"The required column '{col}' is missing from the DataFrame.")

    # Merge province, city, post code, and address into one column if they exist
    if all(col in df.columns for col in ['Province', 'City', 'post code', 'address']):
        df['full_address'] = df['Province'].fillna('') + ', ' + df['City'].fillna('') + ', ' + df['address'].fillna('')

        # Save dropped columns to garbage.csv
        dropped_columns = df[['Province', 'City','post code', 'address']]
        dropped_columns.to_csv('garbage.csv', index=False)

        # Drop the original columns
        df.drop(columns=['Province', 'City','post code', 'address'], inplace=True)
    else:
        print("One or more of the columns 'Province', 'City','post code', 'address' are missing.")

    # Split the data into 4 chunks
    chunks = np.array_split(df, 4)

    # Create a garbage DataFrame to store removed data
    garbage_df = pd.DataFrame(columns=df.columns)

    # Clean each chunk and collect garbage data
    cleaned_chunks = []
    for chunk in chunks:
        # Identify rows with missing or invalid data in the specified columns
        garbage_rows = chunk[chunk[required_columns].isnull().any(axis=1) | chunk['Invalid Email']]
        # Append garbage rows to garbage_df
        garbage_df = pd.concat([garbage_df, garbage_rows])
        # Remove garbage rows from the chunk
        cleaned_chunk = chunk.dropna(subset=required_columns)
        cleaned_chunk = cleaned_chunk[~cleaned_chunk['Invalid Email']]
        # Drop the 'Invalid Email' column as it's no longer needed
        cleaned_chunk = cleaned_chunk.drop(['Invalid Email'], axis=1)
        # Append cleaned chunk to cleaned_chunks list
        cleaned_chunks.append(cleaned_chunk)

    # Save cleaned chunks to separate CSV files
    for i, cleaned_chunk in enumerate(cleaned_chunks):
        cleaned_chunk.to_csv(f'cleaned_chunk_{i+1}.csv', index=False)

    # Save garbage data to a separate CSV file
    garbage_df.to_csv('garbage_data.csv', index=False)

# Example usage
file_path = '/content/translated_car_owners (2).csv'
chunk_and_clean_data(file_path)

import pandas as pd
import numpy as np
import re

# Define a function to check for valid email addresses
def is_valid_email(email):
    """
    Checks if the email address is valid (contains alphanumeric characters and follows basic structure).

    Args:
        email: The email address to check.

    Returns:
        True if the email is valid, False otherwise.
    """
    # Handle missing or non-string values
    if pd.isnull(email) or not isinstance(email, str):
        return False

    # Basic regex for email validation (alphanumeric check included)
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def chunk_and_clean_data(file_path):
    """
    Chunks the data into 4 chunks, cleans the chunks, and creates a garbage file for removed data.

    Args:
        file_path: The path to the CSV file.
    """
    # Read the CSV file (suppressing DtypeWarning)
    df = pd.read_csv(file_path, low_memory=False)

    # Ensure the 'Mail' column exists, regardless of case sensitivity
    df.columns = df.columns.str.strip()  # Remove any leading/trailing spaces
    if 'Mail' not in df.columns:
        raise KeyError("The 'Mail' column is not present in the DataFrame.")
    # Drop specified columns if they exist
    columns_to_drop = ['Monthly salary', 'marriage', 'educate', 'color', 'Unnamed: 21','gender', 'Birthday', 'industry']
    df = df.drop([col for col in columns_to_drop if col in df.columns], axis=1, errors='ignore')

    # Validate emails and create a column for invalid emails
    df['Invalid Email'] = df['Mail'].apply(lambda x: not is_valid_email(x))

    # Define the columns to check for missing values
    required_columns = ['Frame number', 'ID card', 'Motor number', 'Mail']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"The required column '{col}' is missing from the DataFrame.")

    # Merge province, city, post code, and address into one column if they exist
    if all(col in df.columns for col in ['Province', 'City', 'post code', 'address']):
        df['full_address'] = df['Province'].fillna('') + ', ' + df['City'].fillna('') + ', ' + df['address'].fillna('')

        # Save dropped columns to garbage.csv
        dropped_columns = df[['Province', 'City','post code', 'address']]
        dropped_columns.to_csv('garbage.csv', index=False)

        # Drop the original columns
        df.drop(columns=['Province', 'City','post code', 'address'], inplace=True)
    else:
        print("One or more of the columns 'Province', 'City','post code', 'address' are missing.")

    # Split the data into 4 chunks
    chunks = np.array_split(df, 4)

    # Create a garbage DataFrame to store removed data
    garbage_df = pd.DataFrame(columns=df.columns)

    # Clean each chunk and collect garbage data
    cleaned_chunks = []
    for chunk in chunks:
        # Identify rows with missing or invalid data in the specified columns
        garbage_rows = chunk[chunk[required_columns].isnull().any(axis=1) | chunk['Invalid Email']]
        # Append garbage rows to garbage_df
        garbage_df = pd.concat([garbage_df, garbage_rows])
        # Remove garbage rows from the chunk
        cleaned_chunk = chunk.dropna(subset=required_columns)
        cleaned_chunk = cleaned_chunk[~cleaned_chunk['Invalid Email']]
        # Drop the 'Invalid Email' column as it's no longer needed
        cleaned_chunk = cleaned_chunk.drop(['Invalid Email'], axis=1)
        # Append cleaned chunk to cleaned_chunks list
        cleaned_chunks.append(cleaned_chunk)

    # Save cleaned chunks to separate CSV files
    for i, cleaned_chunk in enumerate(cleaned_chunks):
        cleaned_chunk.to_csv(f'cleaned_chunk_{i+1}.csv', index=False)

    # Save garbage data to a separate CSV file
    garbage_df.to_csv('garbage_data.csv', index=False)

# Example usage
file_path = '/content/translated_car_owners (2).csv'
chunk_and_clean_data(file_path)

import pandas as pd
import os

def merge_chunks(directory_path):
    """
    Merges CSV files named 'cleaned_chunk_1.csv' to 'cleaned_chunk_4.csv'
    in the specified directory.

    Args:
        directory_path: The path to the directory containing the CSV files.
    """
    # List to hold DataFrames
    dataframes = []

    # Loop through the files and read them into DataFrames
    # Changed file names to 'cleaned_chunk_1.csv' to 'cleaned_chunk_4.csv'
    for i in range(1, 5):
        file_path = os.path.join(directory_path, f'cleaned_chunk_{i}.csv')
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            dataframes.append(df)
        else:
            print(f"File {file_path} does not exist.")

    # Concatenate all DataFrames
    merged_df = pd.concat(dataframes, ignore_index=True)

    # Save the merged DataFrame to a new CSV file
    merged_file_path = os.path.join(directory_path, 'Merged_Valid.csv')
    merged_df.to_csv(merged_file_path, index=False)
    print(f"Merged file saved to {merged_file_path}")

# Example usage
# Ensure this path is correct and contains the 'cleaned_chunk' files
directory_path = '/content/' # Updated directory path
merge_chunks(directory_path)