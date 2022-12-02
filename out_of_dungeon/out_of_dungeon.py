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


class Castle():

    def __init__(self, name='Сэр', floor=0, room=0, ) -> None:
        self.player_name = name
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
                            if self.floor < self.edge:
                                self.floor += 1
                                if self.pos():
                                    continue
                                else:
                                    self.floor -= 1
                                    break
                            else:
                                break
                        elif way == "восток":
                            if self.room < self.edge:
                                self.room += 1
                                if self.pos():
                                    continue
                                else:
                                    self.room -= 1
                                    break
                            else:
                                break
                        elif way == "юг":
                            if self.floor > 0:
                                self.floor -= 1
                                if self.pos():
                                    continue
                                else:
                                    self.floor += 1
                                    break
                            else:
                                break
                        elif way == "запад":
                            if self.room > 0:
                                self.room -= 1
                                if self.pos():
                                    continue
                                else:
                                    self.room += 1
                                    break
                            else:
                                break
                    return self.pos()
                elif steps == 0:
                    return self.message()
            elif way not in ways:
                return self.warning(way)
        elif way is None or steps is None:
            return self.message()

    
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