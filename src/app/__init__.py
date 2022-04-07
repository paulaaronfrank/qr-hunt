from flask import Flask, send_from_directory, request, render_template, make_response, redirect, url_for, send_file
from .utils import Config, create_qr_code
from uuid import uuid4
from io import BytesIO
import os
import jwt
import pickle


def create_app():
    app = Flask(__name__, static_url_path='')

    @app.route('/assets/<path:path>')
    def send_file(path):
        return send_from_directory('assets', path)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            user_id = str(uuid4())
            username = request.form.get('username')
            token = jwt.encode({'user_id': user_id, 'name': username},
                               Config.SECRET, algorithm='HS256')

            data = pickle.dumps({'name': username, 'codes': set()})
            with open(f'app/users/{user_id}', 'wb') as fp:
                fp.write(data)

            response = make_response(render_template('score.html', name=username, score=0))
            response.set_cookie('token', token)
            return response

        if token := request.cookies.get('token'):
            decoded = jwt.decode(token, Config.SECRET, algorithms=["HS256"])
            with open('app/users/' + decoded['user_id'], 'rb') as fp:
                data = pickle.loads(fp.read())
            score = len(data['codes'])
            return render_template('score.html', name=decoded['name'], score=score)
        return render_template('register.html')

    @app.route('/logout')
    def logout():
        response = make_response(redirect(url_for('index')))
        response.delete_cookie('token')
        return response

    @app.route('/admin')
    def admin():
        return create_qr()

    @app.route('/<qr_id>')
    def check_id(qr_id):
        if token := request.cookies.get('token'):
            qr_codes = [i.split('.')[0] for i in os.listdir(f'{os.getcwd()}/app/codes')]
            if qr_id in qr_codes:
                decoded = jwt.decode(token, Config.SECRET, algorithms=["HS256"])

                with open('app/users/' + decoded['user_id'], 'rb') as fp:
                    data = pickle.loads(fp.read())
                data['codes'].add(qr_id)
                score = len(data['codes'])
                data = pickle.dumps(data)
                with open('app/users/' + decoded['user_id'], 'wb') as fp:
                    fp.write(data)

                return render_template('score.html', name=decoded['name'], score=score)
            return 'Error'
        return 'Please Register First!'

    return app


def list_qr(download=False):
    return


def create_qr():
    qr_id = str(uuid4())
    qr_img = create_qr_code(qr_id)
    img_io = BytesIO()
    qr_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')


def check_qr(id):
    return
