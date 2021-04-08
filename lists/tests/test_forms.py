from django.test import TestCase
from ..forms import ItemForm

class ItemFormTest(TestCase):
    '''тест формы для элемента списка'''

    def test_form_item_input_has_placeholder_and_css_classes(self):
        '''тест: форма отображает текстовое поле ввода'''
        form = ItemForm()
        self.assertIn('placeholder="Введите элемент списка"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())
