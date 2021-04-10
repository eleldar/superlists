from selenium.webdriver.common.keys import Keys
import time
from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
    '''тест макета и стилевого оформления'''

    def test_layout_and_styling(self):
        '''тест макета и стилевого оформления'''
        # Лена открывает домашнюю страницу
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768) # установка фиксированных значений окна
        time.sleep(1)
        # Она замечает, что поле ввода аккуратно центрировано
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual( # assertAlmostEqual помогает нам справиться с погрешностями округления и случайными странностями из-за полос прокрутки и т.п.
            inputbox.location['x'] + inputbox.size['width'] / 2, # смотрим на его размер и расположение и проверяем: расположен ли он посередине страницы
            512,
            delta=10 # погрешность +/-10 пикселов
        )

        # Она начинает новый список и видит, что поле ввода там тоже аккуратно центрировано
        inputbox.send_keys('тестирование')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: тестирование')
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
