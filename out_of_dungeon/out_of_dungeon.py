from logging import warning
from threading import Lock
from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SubmitField
from wtforms.validators import InputRequired, NumberRange


class SingletonMeta(type):
    _instances = {}
    # _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        # with cls._lock:
        if cls not in cls._instances or args or kwargs:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class GameForm(FlaskForm):
    
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
            NumberRange(min=1, max=2, message="Вы не можете сюда двигаться")
            ]
    )

    submit = SubmitField(
        "В путь!"
    )


class Castle(metaclass=SingletonMeta):

    def __init__(self) -> None:
        self.map = self.castle_build()
        self.size = len(self.map)
        self.edge = self.size - 1
        self.floor = 0
        self.room = 0
        self.start = self.map[0][0]
        self.finish = self.map[2][1]
        self.warning = "Вы упёрлись в стену"
        self.congratulation = f"Отлично! Вы выбрались на {self.finish}! Свежий воздух бодрит, а барон Мюнхгаузен приветствует вас!"

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
                            pass
                        else:
                            self.floor -= 1
                    else:
                        break
                elif way == 1:
                    if self.room < self.edge:
                        self.room += 1
                        if self.pos():
                            pass
                        else:
                            self.room -= 1
                    else:
                        break
                elif way == 2:
                    if self.floor > 0:
                        self.floor -= 1
                        if self.pos():
                            pass
                        else:
                            self.floor += 1
                    else:
                        break
                elif way == 3:
                    if self.room > 0:
                        self.room -= 1
                        if self.pos():
                            pass
                        else:
                            self.room += 1
                    else:
                        break
                # self.pos()
        elif steps == 0:
            pass
        return self.message()

    def pos(self):
        return self.map[self.floor][self.room]

    def message(self):
        if self.pos():
            if 0 >= self.floor >= (self.edge - 1) or \
                0 >= self.room >= self.edge:
                return self.warning
            if self.pos() == self.finish:
                return self.congratulation
            else:
                return f'Вы находитесь в комнате {self.pos()}. '
        else:
            return self.warning