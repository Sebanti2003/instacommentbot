import pandas as pd

def load_csv(filename):
    """Load or create a CSV file for storing bot data."""
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        return pd.DataFrame(columns=['id', 'data'])
