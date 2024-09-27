from flask import Flask, render_template

app = Flask(__name__)

posts = [
    {
        'author': 'Author 1',
        'title': 'First Blog Post',
        'content': 'This is the content of the first blog post.',
        'date_posted': 'August 23, 2024'
    },
    {
        'author': 'Author 2',
        'title': 'Second Blog Post',
        'content': 'This is the content of the second blog post.',
        'date_posted': 'August 24, 2024'
    }
]

@app.route("/")
def home():
    return render_template('index.html', posts=posts)

if __name__ == "__main__":
    app.run(debug=True)