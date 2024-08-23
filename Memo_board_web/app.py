from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 게시글을 저장할 리스트
posts = []

@app.route('/')
def home():
    return render_template('home.html', posts=posts)

@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = posts[post_id]
    return render_template('post.html', post=post)

@app.route('/add', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        posts.append({'title': title, 'content': content})
        return redirect(url_for('home'))
    return render_template('add_post.html')

if __name__ == '__main__':
    app.run(debug=True)
