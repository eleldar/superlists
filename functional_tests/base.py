from selenium import webdriver # нужно всегда следить за обновлениями selenium (pip install --upgrade selenium)
                               # и, соотвественно, драйвером geckodriver
from selenium.webdriver.common.keys import Keys
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
import os
from unittest import skip # декоратор пропуска фрагментов кода
from .server_tools import reset_database # функция для обнуления серверной базы данных в промежутках между каждым тестом.

MAX_WAIT = 10 # максимальным количеством времени, которое готовы ожидать. 
              # 10 секунд более чем достаточно для отлавливания любых незначительных сбоев или
              # случайных замедлений

def wait(fn):
    '''декоратор ожидания'''
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    return modified_fn


class FunctionalTest(StaticLiveServerTestCase):
    '''Функциональный тест'''

    def setUp(self):
        '''Установка'''
        self.browser = webdriver.Firefox()
        self.staging_server = os.environ.get('STAGING_SERVER') # адрес реального сервера помещаем в переменную окружения STAGING_SERVER
        if self.staging_server:
            self.live_server_url = 'http://' + self.staging_server # заменяем сервер по умолчанию (self.live_server_url) на адрес реального сервера
            reset_database(self.staging_server) # обнуление базы данных на сервере
    def tearDown(self):
        '''Размонтирование'''
        self.browser.quit()

    def get_item_input_box(self):
        '''получить поле ввода для элемента'''
        return self.browser.find_element_by_id('id_text')

    @wait
    def wait_for_row_in_list_table(self, row_text):
        '''ожидать строку в таблице списка'''
        tag_id = 'id_list_table'
        table = self.browser.find_element_by_id(tag_id)
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def add_list_item(self, item_text):
        '''добавить элемент списка 
        (реализует детали ввода текста в нужное поле)'''
        num_rows = len(self.browser.find_elements_by_css_selector(
            '#id_list_table tr'
        ))
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        item_number = num_rows + 1
        self.wait_for_row_in_list_table(f'{item_number}: {item_text}')

    @wait
    def wait_for(self, fn): # ожидает, что ему будет передана функция
        '''обобщенный метод ожидания'''
        return fn() # возвращаем  значение и выходим из цикла

    @wait
    def wait_to_be_logged_in(self, email):
        """ожидать входа в систему"""
        self.browser.find_element_by_link_text('Выйти')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        """ожидать выхода из системы"""
        self.browser.find_element_by_name('email')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)
