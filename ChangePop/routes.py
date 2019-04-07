from flask import render_template

from ChangePop import models, db, app, user, product

app.register_blueprint(user.bp)
app.register_blueprint(product.bp)

@app.route('/')
def show():
    return render_template('index.html')
