# Book Recommender System

# Import libraries for deploying recommender system
from flask import Flask, render_template, request
import numpy as np
import pickle
import os

# Path to the pickle file
popular_file_path = 'popular.pkl'  # Adjust this path as needed
book_pt = pickle.load(open('book_pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity = pickle.load(open('similarity_score.pkl', 'rb'))
# Ensure the file exists before trying to load it
if not os.path.isfile(popular_file_path):
    raise FileNotFoundError(f"The file {popular_file_path} does not exist.")

# Load the DataFrame
with open(popular_file_path, 'rb') as file:
    popular_df = pickle.load(file)
# Create app
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html",
                           book_name = list(popular_df['Book-Title'].values),
                           author = list(popular_df['Book-Author'].values),
                           image = list(popular_df['Image-URL-M'].values),
                           votes = list(popular_df['Num-Ratings'].values),
                           ratings = list(popular_df['Avg-Ratings'].values),)

@app.route("/recommend")
def recommend_ui():
    return render_template("recommender.html")

@app.route("/contactinfo")
def contactinfo():
    return render_template("contact.html")

@app.route("/recommend_books", methods=["POST"])
def recommend():
    user_input = request.form.get('user_input')

    index = np.where(book_pt.index==user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)[1:6]
    
    data = []
    # iterate items
    for items in similar_items: 
        item = []
        temp_df = books[books['Book-Title']== book_pt.index[items[0]]]
        item.extend(list(temp_df.drop_duplicates("Book-Title")['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates("Book-Title")['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates("Book-Title")["Image-URL-M"].values))

        data.append(item)

    print(data)

    return render_template('recommender.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)  # Removed the extra comma
