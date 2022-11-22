import secrets
from flask import Flask, request, render_template, redirect, session, url_for

from out_of_dungeon import GameForm, Player, Castle

app = Flask(__name__)
app.secret_key =  secrets.token_hex()

@app.route('/')
def index():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    # return 'You are not logged in'
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = GameForm()
    if request.method == 'POST':
        Player.name = form.player_name.data
        session['username'] = Player.name
        return redirect(
            url_for('game', name=Player.name, way=None, steps=None)
            )
    return render_template(
        'index.html',
        form = form
        )

@app.route('/game/<string:name>/', methods=['GET','POST'])
@app.route('/game/<string:name>/<string:way>/<int:steps>/', methods=['GET','POST'])
def game(name, way=None, steps=None):
    if 'username' in session:
        form = GameForm()
        Player.name = name
        if 'floor' and 'room' in session:
            floor = session['floor']
            room = session['room']
            castle = Castle(floor, room)
            if request.method == 'GET':
                way = way
                steps = steps
            elif request.method == 'POST':
                way = form.way.data
                steps = form.steps.data
            castle.move(way, steps)
            session['floor'] = castle.floor
            session['room'] = castle.room
        else:
            session['floor'] = 0
            session['room'] = 0
            castle = Castle()
        return render_template(
            'game.html',
            form = form,
            Player = Player,
            castle = castle,
            way = way,
            steps = steps,
            )
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)