from threading import Lock
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import InputRequired, NumberRange


class GameForm(FlaskForm):
    
    name = StringField(
        "Назовите Ваше имя: ",
        validators=[InputRequired(), NumberRange(33)]
    )

    way = SelectField(
        "Выберите сторону света, в которую хотите отправиться: ",
        coerce = int,
        choices = [
            (0, "Север"),
            (1, "Восток"),
            (2, "Юг"),
            (3, "Запад")
        ],
        render_kw = {
            'class':'form_control',
        },
    )

    steps = IntegerField(
        "Сколько шагов вы хотите пройти?",
        validators = [
            InputRequired(message='Введите количество шагов'),
            NumberRange(min=0, max=5, message="Вы не можете сюда двигаться")
            ]
    )

    submit = SubmitField(
        "В путь!"
    )


class SingletonMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances or args or kwargs:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Player:

    @classmethod
    def __init__(cls, name) -> None:
        cls.name = name


class Castle(Player, metaclass=SingletonMeta):

    def __init__(self, floor=0, room=0, ) -> None:
        if hasattr(Player, 'name'):
            self.name = Player.name
        self.map = self.castle_build()
        self.size = len(self.map)
        self.edge = self.size - 1
        self.floor = floor
        self.room = room
        self.start = self.map[0][0]
        self.finish = self.map[2][1]
        self.warning = ["Вы упёрлись в стену"]

    def castle_build(self):
        return [
            ["Подземелье", "Коридор", "Оружейная"],
            ["Спальня", "Холл", "Кухня"],
            ["", "Балкон", ""],
            ]

    def walk(self, way, steps,):
        if steps > 0:
            for _step in range(1, steps + 1):
                if way == 0:
                    if self.floor < self.edge:
                        self.floor += 1
                        if self.pos():
                            yield self.get_messages()
                        else:
                            self.floor -= 1
                            yield self.warning
                            break
                    else:
                        yield self.warning
                        break
                elif way == 1:
                    if self.room < self.edge:
                        self.room += 1
                        if self.pos():
                            yield self.get_messages()
                        else:
                            self.room -= 1
                            yield self.warning
                            break
                    else:
                        yield self.warning
                        break
                elif way == 2:
                    if self.floor > 0:
                        self.floor -= 1
                        if self.pos():
                            yield self.get_messages()
                        else:
                            self.floor += 1
                            yield self.warning
                            break
                    else:
                        yield self.warning
                        break
                elif way == 3:
                    if self.room > 0:
                        self.room -= 1
                        if self.pos():
                            yield self.get_messages()
                        else:
                            self.room += 1
                            yield self.warning
                            break
                    else:
                        yield self.warning
                        break
                if self.pos() == self.finish:
                    # yield self.get_messages()
                    break
        elif steps == 0:
            yield self.get_messages()

    def pos(self):
        return self.map[self.floor][self.room]

    def get_messages(self):
        message = f"Вы находитесь в комнате {self.pos()}"
        congratulation = f"Отлично, {self.name}! Вы выбрались на {self.finish}! Свежий воздух бодрит, а барон Мюнхгаузен приветствует вас вкуснейшим завтраком!"
        if self.pos() == self.finish:
            return [message, congratulation]

        else:
            return [message]
