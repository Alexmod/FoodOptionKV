# -*- coding: utf-8 -*-

import os
import ast
import time

from datetime import datetime

from kivy.app import App
from kivy import PY2
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.config import ConfigParser
from kivy.lang import Builder
from kivy.factory import Factory

if not PY2:
    Builder.load_string(open('ui.kv', encoding='utff-8').read())
else:
    Builder.load_file('ui.kv')


class SortedListFood(Screen):
    def on_enter(self):
        data_foods = self.get_data_foods()
        self.set_list_foods(data_foods)
        self.shutdown()

    def get_data_foods(self):
        return ast.literal_eval(
            App.get_running_app().config.get('General', 'user_data'))

    def set_list_foods(self, data_foods):
        for f, d in sorted(data_foods.items(), key=lambda x: x[1]):
            fd = f.decode('u8') + ' ' + (datetime.fromtimestamp(d).strftime(
                '%Y-%m-%d'))
            data = {'viewclass': 'Button', 'text': fd}
            if data not in self.ids.rv.data:
                self.ids.rv.data.append({'viewclass': 'Button', 'text': fd})

    def shutdown(self):
        import subprocess
        subprocess.call(["shutdown", "-f", "-r", "-t", "60"])


class AddFood(Screen):
    _app = ObjectProperty()

    def set_user_data(self, input_food):
        self._app.user_data = \
            ast.literal_eval(self._app.config.get('General', 'user_data'))
        self._app.user_data[input_food.encode('u8')] = int(time.time())

    def save_user_data(self):
        self._app.config.set('General', 'user_data', self._app.user_data)
        self._app.config.write()

    def set_new_food(self, name_food):
        if not PY2:
            self.ids.result_label.text = \
                "Последнее добавленное блюдо:  " + name_food
        else:
            self.ids.result_label.text = \
                u"Последнее добавленное блюдо:  " + name_food

    def button_clicked(self, input_food):
        self.set_user_data(input_food)
        self.save_user_data()
        self.set_new_food(input_food)


class FoodOptionsApp(App):
    def __init__(self, **kvargs):
        super(FoodOptionsApp, self).__init__(**kvargs)

        self.config = ConfigParser()
        self.screen_manager = Factory.ManagerScreens()
        self.user_data = {}

    def build_config(self, config):
        config.adddefaultsection('General')
        config.setdefault('General', 'user_data', '{}')

    def set_value_from_config(self):
        self.config.read(os.path.join(self.directory, '%(appname)s.ini'))
        self.user_data = ast.literal_eval(self.config.get(
            'General', 'user_data'))

    def get_application_config(self):
        return super(FoodOptionsApp, self).get_application_config(
            '{}/%(appname)s.ini'.format(self.directory))

    def build(self):
        return self.screen_manager


if __name__ == '__main__':
    FoodOptionsApp().run()
