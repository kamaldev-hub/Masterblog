from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


def get_blog_posts():
    with open('blog_posts.json', 'r') as file:
        return json.load(file)


def save_blog_posts(posts):
    with open('blog_posts.json', 'w') as file:
        json.dump(posts, file, indent=2)


def fetch_post_by_id(post_id):
    posts = get_blog_posts()
    for post in posts:
        if post['id'] == post_id:
            return post
    return None


@app.route('/')
def index():
    blog_posts = get_blog_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        blog_posts = get_blog_posts()
        new_id = max(post['id'] for post in blog_posts) + 1 if blog_posts else 1
        new_post = {
            'id': new_id,
            'title': request.form.get('title'),
            'author': request.form.get('author'),
            'content': request.form.get('content'),
            'likes': 0  # Initialize likes to 0
        }
        blog_posts.append(new_post)
        save_blog_posts(blog_posts)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    blog_posts = get_blog_posts()
    blog_posts = [post for post in blog_posts if post['id'] != post_id]
    save_blog_posts(blog_posts)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        blog_posts = get_blog_posts()
        for p in blog_posts:
            if p['id'] == post_id:
                p['title'] = request.form.get('title')
                p['author'] = request.form.get('author')
                p['content'] = request.form.get('content')
                break
        save_blog_posts(blog_posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


@app.route('/like/<int:post_id>')
def like(post_id):
    blog_posts = get_blog_posts()
    for post in blog_posts:
        if post['id'] == post_id:
            post['likes'] = post.get('likes', 0) + 1
            break
    save_blog_posts(blog_posts)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)