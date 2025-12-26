from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "cok_gizli_super_anahtar"  # Session güvenliği için gerekli

# Hardcoded kullanıcı bilgileri
VALID_USERNAME = "admin"
VALID_PASSWORD = "1234"

@app.route('/')
def home():
    # Eğer kullanıcı zaten giriş yapmışsa dashboard'a yönlendir
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Zaten giriş yapılmışsa
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session['logged_in'] = True
            session['username'] = username
            # Mesaj göstermek istersek (dashboard'da vs)
            # flash('Giriş başarılı!', 'success') 
            return redirect(url_for('dashboard'))
        else:
            flash('Hatalı kullanıcı adı veya şifre!', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
