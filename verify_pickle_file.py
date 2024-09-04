# verify pickle file

import pickle

# Path to your pickle file
file_path = 'popular.pkl'

try:
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    print("File loaded successfully.")
except Exception as e:
    print(f"Error: {e}")
