from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "pwa_cream_premium_style_key"

# 模擬帳號資料夾 (新增對應你測試的帳號)
users = {
    "admin": "1234",
    "riza1234": "12345"
}

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('board'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('board'))
        flash("驗證失敗：您輸入的帳號或密碼不正確！")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users:
            flash("此帳號名稱已被註冊！")
        elif not username or not password:
            flash("欄位不可為空！")
        else:
            users[username] = password
            flash("註冊成功，請使用剛才的密碼登入！")
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/board')
def board():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('board.html', username=session['username'])

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'username' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        username = session['username']
        
        if users[username] == old_password:
            users[username] = new_password
            flash("密碼已修改成功！")
            return redirect(url_for('board'))
        flash("修改失敗：舊密碼輸入錯誤。")
    return render_template('settings.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)