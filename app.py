from flask import Flask, render_template, request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_score = pickle.load(open('similarity_score.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=[round(r, 2) for r in popular_df['avg_rating'].values],  # Round ratings to 2 decimal places
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')

    # Validate user input
    if not user_input or user_input not in pt.index:
        error = 'Invalid input. Please provide a valid book title.'
        return render_template('recommend.html', error=error)

    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    return render_template('recommend.html', data=data)

@app.route('/contact')
def contact():
    return render_template('contacts.html')

if __name__ == '__main__':
    app.run(debug=True)