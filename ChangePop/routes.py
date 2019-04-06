from flask import render_template

from ChangePop import models, db, app, user

app.register_blueprint(user.bp)

@app.route('/')
def show():
    return render_template('index.html')
