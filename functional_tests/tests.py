#! /usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver # нужно всегда следить за обновлениями selenium (pip install --upgrade selenium)
                               # и, соотвественно, драйвером geckodriver
from selenium.webdriver.common.keys import Keys
import time
#from django.test import LiveServerTestCase #import unittest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10 # максимальным количеством времени, которое готовы ожидать. 
              # 10 секунд более чем достаточно для отлавливания любых незначительных сбоев или
              # случайных замедлений


class NewVisitorTest(StaticLiveServerTestCase):
    '''Тест нового посетителя'''

    def setUp(self):
        '''Установка'''
        self.browser = webdriver.Firefox()

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

    def test_layout_and_styling(self):
        '''тест макета и стилевого оформления'''
        # Лена открывает домашнюю страницу
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768) # установка фиксированных значений окна

        # Она замечает, что поле ввода аккуратно центрировано
        inputbox = self.browser.find_element_by_id('id_new_item') #отыскиваем элемент input
        self.assertAlmostEqual( # assertAlmostEqual помогает нам справиться с погрешностями округления и случайными странностями из-за полос прокрутки и т.п.
            inputbox.location['x'] + inputbox.size['width'] / 2, # смотрим на его размер и расположение и проверяем: расположен ли он посередине страницы
            512,
            delta=10 # погрешность +/-10 пикселов
        )

        # Она начинает новый список и видит, что поле ввода там тоже аккуратно центрировано
        inputbox.send_keys('тестирование')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: тестирование')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

    def test_can_start_a_list_for_one_user(self):
        '''тест: можно начать список для одного пользователя'''
        # Лена слышала про крутое новое онлайн-приложение со списком
        # неотложных дел. Она решает оценить его домашнюю страницу
        self.browser.get(self.live_server_url)

        # Она видит, что заголовок и шапка страницы говорят о списках
        # неотложных дел
        self.assertIn('To-Do', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Начать новый список неотложных дел', header_text)

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
        self.wait_for_row_in_list_table('2: Сделать мушку из павлиньих перьев')        
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        '''тест: многочисленные пользователи могут начать списки по разным URL'''

        # Лена начинает новый список
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Купить павлиньи перья')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')

        # Лена замечает, что ее список имеет уникальный URL-адрес
        helen_list_url = self.browser.current_url
        self.assertRegex(helen_list_url, '/lists/.+') # assertRegex – вспомогательная функция из unittest, которая проверяет, 
                                                      # соответствует ли строка регулярному выражению; 
                                                      # используется, чтобы проверить реализацию новой RESTʼовской конструкции.

        # Теперь новый пользователь, Эльдар, приходит на сайт.
        ## Мы используем новый сеанс браузера, тем самым обеспечивая, чтобы никакая
        ## информация от Эдит не прошла через данные cookie и пр.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Эльдар посещает домашнюю страницу. Нет никаких признаков списка Лены
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertNotIn('Сделать мушку', page_text)

        # Эльдар начинает новый список, вводя новый элемент
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Купить молоко')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить молоко')

        # Эльдар получает уникальный URL-адрес
        eldar_list_url = self.browser.current_url
        self.assertRegex(eldar_list_url, '/lists/.+')
        self.assertNotEqual(eldar_list_url, helen_list_url)

        # Опять-таки, нет ни следа от списка Лены
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertIn('Купить молоко', page_text)


        # Удовлетворенные, они оба ложатся спать
        self.browser.quit()
