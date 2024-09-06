from flask import Flask, request, redirect, url_for, render_template, send_from_directory, session
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Chave secreta para a sessão

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Login e senha definidos
USERNAME = 'escolha um login'
PASSWORD = 'escolha uma senha'

# Verifica login
def check_login(username, password):
    return username == USERNAME and password == PASSWORD

# Página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_login(username, password):
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return 'Login ou senha inválidos. Tente novamente.'
    return render_template('login.html')

# Página principal (só acessível após login)
@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

# Upload de arquivos
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'Nenhum arquivo selecionado.'
    file = request.files['file']
    if file.filename == '':
        return 'Nenhum arquivo escolhido.'
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return redirect(url_for('index'))

# Baixar arquivos
@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, host='0.0.0.0')
