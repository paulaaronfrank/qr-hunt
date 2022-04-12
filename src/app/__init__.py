from flask import Flask, send_from_directory, request, render_template, make_response, redirect, url_for, send_file, jsonify
from .utils import Config, create_qr_code
from uuid import uuid4
from io import BytesIO
import os
import jwt
import pickle
import shutil


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
            with open(f'app/users/{user_id}.usr', 'wb') as fp:
                fp.write(data)

            response = make_response(render_template('score.html', name=username, score=0))
            response.set_cookie('user', token)
            return response

        if token := request.cookies.get('user'):
            decoded = jwt.decode(token, Config.SECRET, algorithms=["HS256"])
            try:
                with open('app/users/' + decoded['user_id'] + '.usr', 'rb') as fp:
                    data = pickle.loads(fp.read())
            except:
                data = pickle.dumps({'name': decoded['name'], 'codes': set()})
                with open(f'app/users/{decoded["user_id"]}.usr', 'wb') as fp:
                    fp.write(data)
                data = {'name': decoded['name'], 'codes': set()}
            score = len(data['codes'])
            return render_template('score.html', name=decoded['name'], score=score)
        return render_template('register.html')

    @app.route('/logout')
    def logout():
        response = make_response(redirect(url_for('index')))
        response.delete_cookie('user')
        return response

    @app.route('/admin')
    def admin():
        if request.cookies.get('token'):
            pass
        # ToDo: Login Page if no token // Page QR codes (Add) // User Scores (+ Reset) // Options (Password to register + Reset)
        return render_template('admin_login.html')

    @app.route('/admin/user', methods=['GET', 'DELETE'])
    def admin_user():
        if request.method == 'DELETE':
            for f in os.listdir('app/users'):
                if not f.endswith(".usr"):
                    continue
                os.remove(os.path.join('app/users', f))
            return 'All Users Reset'
        scores = []
        for user in os.listdir('app/users'):
            if user.endswith(".usr"):
                with open('app/users/' + user, 'rb') as fp:
                    data = pickle.loads(fp.read())
                    scores.append((data['name'], len(data['codes'])))
        sorted(scores, key=lambda l: l[1])
        return jsonify(scores)

    @app.route('/admin/qr', methods=['GET', 'POST', 'DELETE'])
    def admin_qr():
        if request.method == 'POST':
            num = min(int(request.args.get('num', 1)), 20)
            if num > 1:
                qrs = []
                for _ in range(num):
                    qrs.append(create_qr())
                return 'created'
            img = create_qr()
            return send_file(img, mimetype='image/png')
        if request.method == 'DELETE':
            for f in os.listdir('app/codes'):
                if not f.endswith(".png"):
                    continue
                os.remove(os.path.join('app/codes', f))
            for f in os.listdir('app/exports'):
                if not f.endswith(".zip"):
                    continue
                os.remove(os.path.join('app/exports', f))
            return 'All Deleted.'
        fn = str(uuid4())
        shutil.make_archive(f'app/exports/{fn}', 'zip', 'app/codes/')
        return send_from_directory('exports', f'{fn}.zip')

    @app.route('/<qr_id>')
    def check_id(qr_id):
        if token := request.cookies.get('user'):
            qr_codes = [i.split('.')[0] for i in os.listdir(f'{os.getcwd()}/app/codes')]
            if qr_id in qr_codes:
                decoded = jwt.decode(token, Config.SECRET, algorithms=["HS256"])

                try:
                    with open('app/users/' + decoded['user_id'] + '.usr', 'rb') as fp:
                        data = pickle.loads(fp.read())
                except:
                    data = {'name': decoded['name'], 'codes': set()}
                data['codes'].add(qr_id)
                score = len(data['codes'])
                data = pickle.dumps(data)
                with open('app/users/' + decoded['user_id'] + '.usr', 'wb') as fp:
                    fp.write(data)

                return render_template('score.html', name=decoded['name'], score=score)
            return 'Error'
        return redirect('index')

    return app


def list_qr(download=False):
    return


def create_qr():
    qr_id = str(uuid4())
    qr_img = create_qr_code(qr_id)
    img_io = BytesIO()
    qr_img.save(img_io, 'PNG')
    img_io.seek(0)
    return img_io
