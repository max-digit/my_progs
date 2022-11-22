# from threading import Lock
from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import InputRequired, Length, NumberRange


class GameForm(FlaskForm):
    
    player_name = StringField(
        "Если готовы, назовите Ваше имя: ",
        validators=[
            InputRequired(message='Введите своё имя'),
            Length(min=2, max=33, message=f'Выберите имя длиной от 2 до 33 символов')]
    )

    way = SelectField(
        "Выберите сторону света, в которую хотите отправиться: ",
        coerce = str,
        choices = [
            ("север", "Север"),
            ("восток", "Восток"),
            ("юг", "Юг"),
            ("запад", "Запад")
        ],
        render_kw = {
            'class':'form_control',
        },
    )

    day = IntegerField(
        "Введите число месяца: ",
        validators=[
            InputRequired(),
            NumberRange(min=1, max=32)
        ],
        # default = 1
    )

    month = SelectField(
        "Выберите месяц: ",
        validators=[InputRequired()],
        choices=(
            "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь",
        ),
    )

    steps = IntegerField(
        "Сколько шагов вы хотите пройти?",
        validators = [
            InputRequired(message='Введите количество шагов'),
            NumberRange(min=1, message="Количество шагов должно быть больше нуля")
            ],
            default=1
    )

    submit = SubmitField(
        "В путь!"
    )


"""class SingletonMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances or args or kwargs:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]"""


class Player:

    @classmethod
    def __init__(cls, name) -> None:
        cls.name = name


class Castle(Player):

    def __init__(self, floor=0, room=0, ) -> None:
        if hasattr(Player, 'name'):
            self.player_name = getattr(Player, 'name')
        else:
            self.player_name = 'Сэр'
        self.map = self.castle_build()
        self.start = self.map[0][0]
        self.finish = self.map[2][1]
        self.floor = floor
        self.room = room
        self.position = self.map[self.floor][self.room]
        self.size = len(self.map)
        self.edge = self.size - 1

    def castle_build(self):
        return [
            ["Погреб", "Коридор", "Оружейная"],
            ["Спальня", "Холл", "Кухня"],
            ["", "Балкон", ""],
            ]

    def move(self, way, steps):
        ways = ("север", "восток", "юг", "запад")
        if way is not None and steps is not None:
            if way in ways:
                if steps > 0:
                    for _step in range(1, steps + 1):
                        if way == "север":
                            # yield from self.walk_north(steps)
                            if self.floor < self.edge:
                                self.floor += 1
                                if self.pos():
                                    # yield from self.pos()
                                    continue
                                else:
                                    self.floor -= 1
                                    # yield from self.pos()
                                    break
                            else:
                                # yield from self.pos()
                                break
                        elif way == "восток":
                            # yield from self.walk_east(steps)
                            if self.room < self.edge:
                                self.room += 1
                                if self.pos():
                                    # yield from self.pos()
                                    continue
                                else:
                                    self.room -= 1
                                    # yield from self.pos()
                                    break
                            else:
                                # yield from self.pos()
                                break
                        elif way == "юг":
                            # yield from self.walk_south(steps)
                            if self.floor > 0:
                                self.floor -= 1
                                if self.pos():
                                    # yield from self.pos()
                                    continue
                                else:
                                    self.floor += 1
                                    # yield from self.pos()
                                    break
                            else:
                                # yield from self.pos()
                                break
                        elif way == "запад":
                            # yield from self.walk_west(steps)
                            if self.room > 0:
                                self.room -= 1
                                if self.pos():
                                    # yield from self.pos()
                                    continue
                                else:
                                    self.room += 1
                                    # yield from self.pos()
                                    break
                            else:
                                # yield from self.pos()
                                break
                    return self.pos()
                elif steps == 0:
                    return self.message()
            elif way not in ways:
                return self.warning(way)
        elif way is None or steps is None:
            return self.message()

    def walk_north(self, steps):
        for _step in range(1, steps + 1):
            if self.floor < self.edge:
                self.floor += 1
                if self.pos():
                    yield self.message()
                else:
                    self.floor -= 1
                    yield self.notice()
                    break
            else:
                yield self.notice()
                break
            if self.pos() == self.finish:
                yield self.congratulation()
                break

    def walk_east(self, steps):
        for _step in range(1, steps + 1):
            if self.room < self.edge:
                self.room += 1
                if self.pos():
                    yield self.message()
                else:
                    self.room -= 1
                    yield self.notice()
                    break
            else:
                yield self.notice()
                break
            if self.pos() == self.finish:
                yield self.congratulation()
                break

    def walk_south(self, steps):
        for _step in range(1, steps + 1):
            if self.floor > 0:
                self.floor -= 1
                if self.pos():
                    yield self.message()
                else:
                    self.floor += 1
                    yield self.notice()
                    break
            else:
                yield self.notice()
                break
            if self.pos() == self.finish:
                yield self.congratulation()
                break

    def walk_west(self, steps):
        for _step in range(1, steps + 1):
            if self.room > 0:
                self.room -= 1
                if self.pos():
                    yield self.message()
                else:
                    self.room += 1
                    yield self.notice()
                    break
            else:
                yield self.notice()
                break
            if self.pos() == self.finish:
                yield self.congratulation()
                break

    def coord(self):
        return {'floor':self.floor, 'room':self.room}

    def pos(self):
        return self.map[self.floor][self.room]

    def message(self):
        return f'Вы в комнате {self.pos()}'

    def notice(self):
        return f'Вы упёрлись в стену комнаты {self.pos()}'
    
    def warning(self, way):
        return f'Такой стороны света ({way}) не существует. Проверьте введенные данные'

    def congratulation(self):
        return f'Отлично! Вы выбрались на {self.finish}! Свежий воздух бодрит, а барон Мюнхгаузен приветствует Вас вкуснейшим завтраком!'