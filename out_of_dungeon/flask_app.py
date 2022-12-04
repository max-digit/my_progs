import secrets
from flask import Flask, request, render_template, redirect, session, url_for

from out_of_dungeon import GameForm, Castle

app = Flask(__name__)
app.secret_key =  secrets.token_hex()

@app.route('/')
def index():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = GameForm()
    if request.method == 'POST':
        user_name = form.player_name.data
        session['username'] = user_name
        return redirect(
            url_for('game', name=user_name, way=None, steps=None)
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
        player_name = name
        if form.day.data == 32 and form.month.data == "Май":
            session['castle_map_opened'] = True
        print(session)
        if 'floor' and 'room' in session:
            floor = session['floor']
            room = session['room']
            castle = Castle(player_name, floor, room)
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
            castle = Castle(player_name)
        return render_template(
            'game.html',
            form = form,
            castle = castle,
            )
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)