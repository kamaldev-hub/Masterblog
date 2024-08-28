from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

users = {
    'Alice': {'age': 25, 'country': 'USA'},
    'Bob': {'age': 30, 'country': 'UK'},
    'Charlie': {'age': 35, 'country': 'Australia'}
}


@app.route('/')
def index():
    name = request.args.get('name', 'Guest')
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_info = users.get(name, {})
    return render_template('index.html', name=name, current_time=current_time, user_info=user_info)


@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/all-users')
def all_users():
    return render_template('all_users.html', users=users)


@app.route('/update-country', methods=['GET', 'POST'])
def update_country():
    if request.method == 'POST':
        name = request.form['name']
        country = request.form['country']
        if name in users:
            users[name]['country'] = country
            return redirect(url_for('all_users'))
        else:
            return f"User {name} not found.", 404
    return render_template('update_country.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
