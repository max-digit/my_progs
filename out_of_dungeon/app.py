from flask import Flask, request, render_template, redirect, url_for

from out_of_dungeon import GameForm, Player, Castle
from config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/', methods=['GET', 'POST'])
def index():
    form = GameForm()
    name = form.name
    Player.name = name.data
    Castle(floor=0, room=0)
    if request.method == 'POST':
        return redirect(url_for('game'))
    return render_template(
        'index.html',
        form = form
        )


@app.route('/game/', methods=['GET','POST'])
def game():
    form = GameForm()
    castle = Castle()
    if request.method == 'GET':
        return render_template(
        'game.html',
        form = form,
        )
    return render_template(
        'game.html',
        form = form,
        castle = castle,
        )



@app.route('/game/<int:way>/<int:steps>/', methods=['GET', 'POST'])
def get_off(way, steps):
    form = GameForm()
    castle = Castle()
    return render_template(
        'game.html',
        form = form,
        castle = castle,
    )

if __name__ == '__main__':
    app.run(debug=True)
