from flask import Flask, url_for, render_template


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    from ChangePop import otro
    app.register_blueprint(otro.bp)

    @app.route('/')
    def show():
        return render_template('index.html')

    @app.route('/<path:subpath>')
    def show2(subpath):
        return render_template(subpath+'.html')

    return app
