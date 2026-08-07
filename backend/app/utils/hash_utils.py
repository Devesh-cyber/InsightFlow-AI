import hashlib

def generate_dataframe_hash(df):

    dataframe_bytes = df.to_csv(index=False).encode()

    return hashlib.sha256(
        dataframe_bytes
    ).hexdigest()