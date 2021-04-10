from selenium import webdriver # нужно всегда следить за обновлениями selenium (pip install --upgrade selenium)
                               # и, соотвественно, драйвером geckodriver
from selenium.webdriver.common.keys import Keys
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
import os
from unittest import skip # декоратор пропуска фрагментов кода

MAX_WAIT = 10 # максимальным количеством времени, которое готовы ожидать. 
              # 10 секунд более чем достаточно для отлавливания любых незначительных сбоев или
              # случайных замедлений

class FunctionalTest(StaticLiveServerTestCase):
    '''Функциональный тест'''

    def setUp(self):
        '''Установка'''
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER') # адрес реального сервера помещаем в переменную окружения STAGING_SERVER
        if staging_server:
            self.live_server_url = 'http://' + staging_server # заменяем сервер по умолчанию (self.live_server_url) на адрес реального сервера

    def tearDown(self):
        '''Размонтирование'''
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        '''ожидать строку в таблице списка'''
        start_time = time.time()
        while True:
            try:
                tag_id = 'id_list_table'
                table = self.browser.find_element_by_id(tag_id)
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except(AssertionError, WebDriverException) as e: # отлавливаем два типа исключений:
                                                             # 1. WebDriverException для случая, когдастраница не загрузилась и
                                                             # Selenium не может найти табличный элемент на странице,
                                                             # 2. AssertionError – для случая, когда таблица имеется,
                                                             # но это, возможно, таблица до перезагрузок страницы,
                                                             # поэтому в ней пока нет нашей строки
                if time.time() - start_time > MAX_WAIT: # 6
                    raise e     # поднимаем исключение и даем ему «всплыть» в тесте при превышении лимита времени
                time.sleep(0.5) # если мы отлавливаем исключение, то ожидаем в течение короткого периода
                                # и в цикле делаем повторную попытку

    def wait_for(self, fn): # ожидает, что ему будет передана функция
        '''обобщенный метод ожидания'''
        start_time = time.time()
        while True:
            try: # тело блока try/except используется для вызова функции, которую передали
                return fn() # возвращаем  значение и выходим из цикла
            except(AssertionError, WebDriverException) as e: # отлавливаем два типа исключений:
                                                             # 1. WebDriverException для случая, когда страница не загрузилась и
                                                             # Selenium не может найти табличный элемент на странице,
                                                             # 2. AssertionError – для случая, когда таблица имеется,
                                                             # но это, возможно, таблица до перезагрузок страницы,
                                                             # поэтому в ней пока нет нашей строки
                if time.time() - start_time > MAX_WAIT: # 6
                    raise e     # поднимаем исключение и даем ему «всплыть» в тесте при превышении лимита времени
                time.sleep(0.5) # если мы отлавливаем исключение, то ожидаем в течение короткого периода
                                # и в цикле делаем повторную попытку

    def get_item_input_box(self):
        '''получить поле ввода для элемента'''
        return self.browser.find_element_by_id('id_text')
