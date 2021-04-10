from selenium.webdriver.common.keys import Keys
from unittest import skip # декоратор пропуска фрагментов кода
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    '''тест валидации элмента списка на непустоту и корректирровку'''


    def test_cannot_add_empty_list_items(self):
        '''тест: нельзя добавлять пустые элементы списка'''
        # Лена открывает домашнюю страницу и случайно пытается отправить
        # пустой элемент списка. Она нажимает Enter на пустом поле ввода
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Браузер перехватывает запрос и не загружает страницу со списком
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:invalid' # invalid псевдоселектор к недопустимым входным данным
        ))

        # Лена начинает набирать текст нового элемента и ошибка исчезает
        self.get_item_input_box().send_keys('Купить молоко')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:valid' #  valid псевдоселектор к допустимым входным данным
        ))

        # И она может отправить его успешно
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить молоко')

        # Далее, находясь на странице списка (не домашняя страница) Лена решает ввести пустой элемент
        self.get_item_input_box().send_keys(Keys.ENTER)

        # И снова браузер не подчиниться
        self.wait_for_row_in_list_table('1: Купить молоко')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:invalid' #  invalid псевдоселектор к недопустимым входным данным
        ))

        # И она может это исправить, заполнив поле каким-то текстом
        self.get_item_input_box().send_keys('Купить хлеб')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:valid' #  valid псевдоселектор к допустимым входным данным
        ))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить молоко')
        self.wait_for_row_in_list_table('2: Купить хлеб')
