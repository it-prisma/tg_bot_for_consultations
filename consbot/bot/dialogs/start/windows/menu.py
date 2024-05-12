from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Row, Start
from aiogram_dialog.widgets.text import Const

from consbot.bot.dialogs.messages import START_MESSAGE
from consbot.bot.dialogs.states import RegisterConsultantSG, RegisterRegularSG

window = Window(
    Const(START_MESSAGE),
    Row(
        Start(Const("Хочу помочь"), state=RegisterConsultantSG.input_name),
        Start(Const("Нужна помощь"), state=RegisterRegularSG.input_name),
    ),
)
