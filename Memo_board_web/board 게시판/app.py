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
    return render_template('post.html', post=post, post_id=post_id)  # post_id 전달


@app.route('/add', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        posts.append({'title': title, 'content': content, 'comments': []})  # comments 리스트 추가
        return redirect(url_for('home'))
    return render_template('add_post.html')

@app.route('/post/<int:post_id>/comment', methods=['POST'])
def add_comment(post_id):
    comment = request.form['comment']
    posts[post_id]['comments'].append(comment)
    return redirect(url_for('view_post', post_id=post_id))

if __name__ == '__main__':
    app.run(debug=True)
