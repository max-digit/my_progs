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
        if form.validate_on_submit:
            return redirect(url_for('game', name=Player.name, way=None, steps=None))
    return render_template(
        'index.html',
        form = form
        )

@app.route('/game/<string:name>/', methods=['GET','POST'])
@app.route('/game/<string:name>/<int:way>/<int:steps>/', methods=['GET','POST'])
def game(name, way=None, steps=None):
    form = GameForm()
    Player.name = name
    castle = Castle()
    if request.method == 'GET':
        if way is not None and steps is not None:
            way = way
            steps = steps
    elif request.method == 'POST':
        way = form.way.data
        steps = form.steps.data
    walk = castle.move(way, steps)
    return render_template(
        'game.html',
        form = form,
        Player = Player,
        castle = castle,
        way = way,
        steps = steps,
        walk = walk,
        )


if __name__ == '__main__':
    app.run(debug=True)
