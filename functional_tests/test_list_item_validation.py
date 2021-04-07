from selenium.webdriver.common.keys import Keys
from unittest import skip # декоратор пропуска фрагментов кода
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    '''тест валидации элмента списка на непустоту и корректирровку'''

    #@skip
    def test_cannot_add_empty_list_items(self):
        '''тест: нельзя добавлять пустые элементы списка'''
        # Лена открывает домашнюю страницу и случайно пытается отправить
        # пустой элемент списка. Она нажимает Enter на пустом поле ввода
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # Домашняя страница обновляется и появляется сообщение об ошибке,
        # которое говорит, что элемены списка не должны быть пустыми
        #self.assertEqual(
        #    self.browser.find_element_by_css_selector('.has-error').text, # указываем, что собираемся использовать класс CSS под названием .has-error, чтобы отметить текст с ошибкой
        #    'Вы не можете вводить пустую строку!' # проверка, что наша ошибка отображает сообщение
        #)
        self.wait_for(lambda: self.assertEqual( # Вместо явного вызова утверждения заворачиваем его в лямбда-функцию и передаем методу wait_for, который определим в base
            self.browser.find_element_by_css_selector('.has-error').text,
            'Вы не можете вводить пустую строку!'
        ))

        # Она пробует снова, теперь с каким-то текстом для элемента,
        # и теперь сайт не выдает ошибку
        self.browser.find_element_by_id('id_new_item').send_keys('Купить молоко')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить молоко')

        # Далее, находясь на странице списка (не домашняя страница) Лена решает ввести пустой элемент
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # Она получает аналогичное предупреждение на странице списка
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            'Вы не можете вводить пустую строку!'
        ))

        # И она может его исправить, заполнив поле каким-то текстом
        self.browser.find_element_by_id('id_new_item').send_keys('Купить хлеб')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить молоко')
        self.wait_for_row_in_list_table('2: Купить хлеб')
