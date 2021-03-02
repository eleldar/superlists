#! /usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase): # 1; метод, который Selenium предоставляет для исследования веб-страниц
    '''Тест нового посетителя'''

    def setUp(self):
        '''Установка'''
        self.browser = webdriver.Firefox()

    def tearDown(self):
        '''Размонтирование'''
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self): 
        '''тест: можно начать список и получить его позже'''
        # Лена слышала про крутое новое онлайн-приложение со списком
        # неотложных дел. Она решает оценить его домашнюю страницу
        self.browser.get('http://localhost:8000')

        # Она видит, что заголовок и шапка страницы говорят о списках
        # неотложных дел
        self.assertIn('To-Do', self.browser.title) 

        header_text = self.browser.find_element_by_tag_name('h1').text # 1; методов, которые Selenium предоставляет для исследования веб-страниц; вернет несколько элементов, а не один)
        self.assertIn('To-Do', header_text)

        # Ей сразу же предлагается ввести элемент списка
        inputbox = self.browser.find_element_by_id('id_new_item') # 1; методов, которые Selenium предоставляет для исследования веб-страниц
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Введите элемент списка'
        )

        # Она набирает в текстовом поле "Купить павлиньи перья" (ее хобби –
        # вязание рыболовных мушек)
        inputbox.send_keys('Купить павлиньи перья') # 2; используем send_keys , который является принятым в Selenium способом ввода данных в поля ввода input

        # Когда она нажимает enter, страница обновляется, и теперь страница
        # содержит "1: Купить павлиньи перья" в качестве элемента списка
        inputbox.send_keys(Keys.ENTER) # 3; класс Keys позволяет отправлять специальные клавиши наподобие Enter
        time.sleep(5) # 4; гарантирует, что браузер закончил загружать новую страницу, преж­де чем мы сделаем какие-либо утверждения. Это называется явным ожиданием!

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr') # 1
        self.assertTrue(
            any(row.text == '1: Купить павлиньи перья' for row in rows),
            "Новый элемент списка не появился в таблице"
        )

        # Текстовое поле по-прежнему приглашает ее добавить еще один элемент.
        # Она вводит "Сделать мушку из павлиньих перьев" (Лена очень методична)

        self.fail('Закончить тест!')

        # Страница снова обновляется, и теперь показывает оба элемента ее списка

        # Лене интересно, запомнит ли сайт ее список. Далее она видит, что
        # сайт сгенерировал для нее уникальный URL-адрес – об этом
        # выводится небольшой текст с объяснениями.

        # Она посещает этот URL-адрес – ее список по-прежнему там.

        # Удовлетворенная, она снова ложится спать
if __name__ == '__main__':
    unittest.main(warnings='ignore') # 7; warnings='ignore' подавляет излишние предупреждающие сообщения Resourcewarning , которые выдавались во время написания
