from flask import Flask, request, render_template

from out_of_dungeon import GameForm, Castle
from config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/game/', methods=['GET','POST'])
def game():
    form = GameForm()
    castle = Castle()
    if request.method == 'GET':
        return render_template(
            'game.html',
            form = form,
            # castle = castle,
        )
    elif request.method == 'POST':
        way = form.way.data
        steps = form.steps.data
        return render_template(
            'game.html',
            form = form,
            castle = castle,
            positions = castle.walk(way, steps)
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
