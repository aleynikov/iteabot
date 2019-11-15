beginning_kb = {
    'news': 'Последние новости',
    'products': 'Продукты',
    'sales': 'Продукты со скидкой',
    'about': 'О нас'
}

from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from models import models

class InlineKB(InlineKeyboardMarkup):
    queries = {
        'root': models.Category.get_root_categories()
    }

    def __init__(self, named_arg, lookup_field='id', title_field='title', row_width=3, iterable=None, key=None):
        if all([iterable, key]):
            raise ValueError('Only one pf fields (iterable, key) can be set ')

        super().__init__(row_width=row_width)
        self._iterable = iterable
        self._named_arg = named_arg
        self._lookup_field = lookup_field
        self._title_field = title_field
        self._query = self.queries.get(key)

    def gen_kb(self):
        buttons = []

        if not self._iterable:
            self._iterable = self._query

        for i in self._iterable:
            buttons.append(InlineKeyboardButton(
                text=str(getattr(i, self._title_field)),
                callback_data = f'{self._named_arg}_' + str(getattr(i, self._lookup_field))
            ))

        self.add(*buttons)
        return self

    def gen_root_kb(self):
        if not self._iterable:
            self._iterable = models.Category.get_root_categories()
            return self.gen_kb()
        raise ValueError('Not iterable set')

class ReplyKB(ReplyKeyboardMarkup):
    def __init__(self, one_time_keyboard=True, resize_keyboard=True, row_width=3):
        super().__init__(one_time_keyboard=one_time_keyboard,
            resize_keyboard=resize_keyboard,
            row_width=row_width)

    def get_beginning_kb(self):
        return self.gen_kb(*beginning_kb.values())

    def gen_kb(self, *args):
        buttons = [KeyboardButton(kb) for kb in args]
        self.add(*buttons)
        return self