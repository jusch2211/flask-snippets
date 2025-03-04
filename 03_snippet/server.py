from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# JSON-Objekt für Benutzer und Rollen
USERS = {
    "admin": {"password": "1234", "role": "Administrator"},
    "user": {"password": "password", "role": "Nutzer"}
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = USERS.get(username)
        if user and user['password'] == password:
            session['username'] = username
            session['role'] = user['role']
            return redirect(url_for('homepage'))
        else:
            flash('Ungültige Anmeldedaten. Bitte versuchen Sie es erneut.')

    return render_template('login.html')

@app.route('/homepage')
def homepage():
    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('homepage.html', username=session['username'], role=session['role'])

@app.route('/secret_admin_shit')
def secret_admin_shit():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    return render_template('secret_admin_shit.html',username=session['username'], role=session['role'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Kontextprozessor für Menü
def inject_menu():
    menu_links = [
        {"name": "Startseite", "url": url_for('homepage')},
        {"name": "Abmelden", "url": url_for('logout')}
    ]
    if 'role' in session and session['role'] == 'Administrator':
        menu_links.append({"name": "Secret Stuff", "url": url_for('secret_admin_shit')})
    return {"menu_links": menu_links}

app.context_processor(inject_menu)

if __name__ == '__main__':
    app.run(debug=True)
