def preprocess_dataset(df):
    # Remove duplicate rows
    df = df.drop_duplicates()

    # Handle missing values
    df = df.dropna()

    # Standardize text data (lowercase)
    df['score'] = df['score'].str.lower()
    df['school'] = df['school'].str.lower()
    df['city'] = df['city'].str.lower()

    # Convert 'yes' and 'no' to boolean values
    df['perfect_score'] = df['perfect_score'].map({'yes': True, 'not': False})
    if 'enter_elfak' in df:
        df['enter_elfak'] = df['enter_elfak'].map({'yes': True, 'not': False})

    return df

