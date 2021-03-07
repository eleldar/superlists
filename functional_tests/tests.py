#! /usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver # нужно всегда следить за обновлениями selenium (pip install --upgrade selenium)
                               # и, соотвественно, драйвером geckodriver
from selenium.webdriver.common.keys import Keys
import time
from django.test import LiveServerTestCase #import unittest
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10 # максимальным количеством времени, которое готовы ожидать. 
              # 10 секунд более чем достаточно для отлавливания любых незначительных сбоев или
              # случайных замедлений


class NewVisitorTest(LiveServerTestCase):
    '''Тест нового посетителя'''

    def setUp(self):
        '''Установка'''
        self.browser = webdriver.Firefox()

    def tearDown(self):
        '''Размонтирование'''
        self.browser.quit()

   # def check_for_row_in_list_table(self, row_text):
   #     '''подтверждение строки в таблице списка'''
   #     table = self.browser.find_element_by_id('id_list_table')
   #     rows = table.find_elements_by_tag_name('tr')
   #     self.assertIn(row_text, [row.text for row in rows])
    def wait_for_row_in_list_table(self, row_text):
        '''ождать строку в таблице списка'''
        start_time = time.time()
        while True:
            try:
                # row_text = 'foo' # специально для ошибки
                tag_id = 'id_list_table' #'id_nothing' # специально для ошибки
                table = self.browser.find_element_by_id(tag_id)
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return # если выполняется тестирующее утверждение их проходит, то
                       # возвращаемся из функции и выходим из цикла
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


    def test_can_start_a_list_and_retrieve_it_later(self):
        '''тест: можно начать список и получить его позже'''
        # Лена слышала про крутое новое онлайн-приложение со списком
        # неотложных дел. Она решает оценить его домашнюю страницу
        self.browser.get(self.live_server_url)

        # Она видит, что заголовок и шапка страницы говорят о списках
        # неотложных дел
        self.assertIn('To-Do', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Ей сразу же предлагается ввести элемент списка
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Введите элемент списка'
        )

        # Она набирает в текстовом поле "Купить павлиньи перья" (ее хобби –
        # вязание рыболовных мушек)
        inputbox.send_keys('Купить павлиньи перья')

        # Когда она нажимает enter, страница обновляется, и теперь страница
        # содержит "1: Купить павлиньи перья" в качестве элемента списка
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')

        # Текстовое поле по-прежнему приглашает ее добавить еще один элемент.
        # Она вводит "Сделать мушку из павлиньих перьев" (Лена очень методична)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Сделать мушку из павлиньих перьев')
        inputbox.send_keys(Keys.ENTER)

        # Страница снова обновляется, и теперь показывает оба элемента ее списка
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')
        self.wait_for_row_in_list_table('2: Сделать мушку из павлиньих перьев')

        # Лене интересно, запомнит ли сайт ее список. Далее она видит, что
        # сайт сгенерировал для нее уникальный URL-адрес – об этом
        # выводится небольшой текст с объяснениями.
        self.fail('Закончить тест!')

        # Она посещает этот URL-адрес – ее список по-прежнему там.

        # Удовлетворенная, она снова ложится спать
