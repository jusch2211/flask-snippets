from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# JSON-Objekt für Benutzer und Rollen
USERS = {
    "admin": {"password": "1234", "role": "Administrator"},
    "user": {"password": "password", "role": "Nutzer"}
}

# In-Memory-Datenbank für Abfragen
queries = []

# Nutzer-Votes speichern
user_votes = {}  # Format: {username: {query_index: vote_option}}

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

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/queries/create', methods=['GET', 'POST'])
def create_query():
    if 'username' not in session or session['role'] != 'Administrator':
        flash('Nur Administratoren dürfen Abfragen erstellen.')
        return redirect(url_for('homepage'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        queries.append({
            "title": title,
            "description": description,
            "votes": {"agree": 0, "disagree": 0, "abstain": 0}
        })
        flash('Abfrage erfolgreich erstellt!')
        return redirect(url_for('read_queries'))

    return render_template('queries/create.html')

@app.route('/queries')
def read_queries():
    if 'username' not in session:
        return redirect(url_for('login'))

    user_vote_data = user_votes.get(session['username'], {})
    return render_template('queries/read.html', queries=queries, user_vote_data=user_vote_data)

@app.route('/queries/vote/<int:index>', methods=['POST'])
def vote_query(index):
    if 'username' not in session or session['role'] == 'Administrator':
        flash('Nur Nutzer dürfen abstimmen.')
        return redirect(url_for('read_queries'))

    if index < 0 or index >= len(queries):
        flash('Ungültige Abfrage.')
        return redirect(url_for('read_queries'))

    vote = request.form['vote']
    if vote in queries[index]['votes']:
        username = session['username']
        user_vote_data = user_votes.setdefault(username, {})

        # Wenn bereits abgestimmt wurde, vorherige Stimme entfernen
        previous_vote = user_vote_data.get(index)
        if previous_vote:
            queries[index]['votes'][previous_vote] -= 1

        # Neue Stimme setzen
        queries[index]['votes'][vote] += 1
        user_vote_data[index] = vote

        flash('Abstimmung erfolgreich!')
    else:
        flash('Ungültige Abstimmungsoption.')

    return redirect(url_for('read_queries'))

# Kontextprozessor für Menü
def inject_menu():
    menu_links = [
        {"name": "Startseite", "url": url_for('homepage')},
        {"name": "Abfragen", "url": url_for('read_queries')},
        {"name": "Abmelden", "url": url_for('logout')}
    ]
    if 'role' in session and session['role'] == 'Administrator':
        menu_links.append({"name": "Neue Abfrage", "url": url_for('create_query')})
    return {"menu_links": menu_links}

app.context_processor(inject_menu)

if __name__ == '__main__':
    app.run(debug=True)
