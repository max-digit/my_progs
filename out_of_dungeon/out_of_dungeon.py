from threading import Lock

from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import InputRequired, Length, NumberRange


class GameForm(FlaskForm):
    
    name = StringField(
        "Если готовы, назовите Ваше имя: ",
        validators=[
            InputRequired(message='Введите своё имя'),
            Length(max=33, message=f'Выберите имя покороче')]
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
            self.name = getattr(Player, 'name')
        else:
            self.name = 'Сэр'
        self.map = self.castle_build()
        self.size = len(self.map)
        self.edge = self.size - 1
        self.floor = floor
        self.room = room
        self.start = self.map[0][0]
        self.finish = self.map[2][1]

    def castle_build(self):
        return [
            ["Погреб", "Коридор", "Оружейная"],
            ["Спальня", "Холл", "Кухня"],
            ["", "Балкон", ""],
            ]

    def move(self, way: str, steps: int):
        ways = ("север", "восток", "юг", "запад")
        if way is not None and steps is not None:
            if way in ways:
                if steps > 0:
                    if way == "север":
                        yield from self.walk_north(steps)
                    elif way == "восток":
                        yield from self.walk_east(steps)
                    elif way == "юг":
                        yield from self.walk_south(steps)
                    elif way == "запад":
                        yield from self.walk_west(steps)
                elif steps == 0:
                    yield self.get_message()
            elif way not in ways:
                yield self.get_warning(way)
        elif way is None or steps is None:
            yield self.get_message()

    def walk_north(self, steps):
        for _step in range(1, steps + 1):
            if self.floor < self.edge:
                self.floor += 1
                if self.pos():
                    yield self.get_message()
                else:
                    self.floor -= 1
                    yield self.get_notice()
                    break
            else:
                yield self.get_notice()
                break
            if self.pos() == self.finish:
                yield self.get_congratulation()
                break

    def walk_east(self, steps):
        for _step in range(1, steps + 1):
            if self.room < self.edge:
                self.room += 1
                if self.pos():
                    yield self.get_message()
                else:
                    self.room -= 1
                    yield self.get_notice()
                    break
            else:
                yield self.get_notice()
                break
            if self.pos() == self.finish:
                yield self.get_congratulation()
                break

    def walk_south(self, steps):
        for _step in range(1, steps + 1):
            if self.floor > 0:
                self.floor -= 1
                if self.pos():
                    yield self.get_message()
                else:
                    self.floor += 1
                    yield self.get_notice()
                    break
            else:
                yield self.get_notice()
                break
            if self.pos() == self.finish:
                yield self.get_congratulation()
                break

    def walk_west(self, steps):
        for _step in range(1, steps + 1):
            if self.room > 0:
                self.room -= 1
                if self.pos():
                    yield self.get_message()
                else:
                    self.room += 1
                    yield self.get_notice()
                    break
            else:
                yield self.get_notice()
                break
            if self.pos() == self.finish:
                yield self.get_congratulation()
                break

    def pos(self):
        return self.map[self.floor][self.room]

    def get_message(self):
        return f'Вы в комнате {self.pos()}'

    def get_notice(self):
        return f'Вы упёрлись в стену комнаты {self.pos()}'
    
    def get_warning(self, way):
        return f'Такой стороны света ({way}) не существует. Проверьте введенные данные'

    def get_congratulation(self):
        return f'Отлично, {self.name}! Вы выбрались на {self.finish}! Свежий воздух бодрит, а барон Мюнхгаузен приветствует вас вкуснейшим завтраком!'