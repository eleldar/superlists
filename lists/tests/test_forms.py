from django.test import TestCase
from ..forms import ItemForm, EMPTY_ITEM_ERROR

class ItemFormTest(TestCase):
    '''тест формы для элемента списка'''

    def test_form_item_input_has_placeholder_and_css_classes(self):
        '''тест: форма отображает текстовое поле ввода'''
        form = ItemForm()
        self.assertIn('placeholder="Введите элемент списка"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        '''тест: валидация формы для пустых элементов'''
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid()) # form.is_valid() возвращает True или False;
                                          # также имеет побочный эффект, заключающийся в валидации входных данных
                                          # и заполнения атрибута errors. Это словарь, который отображает имена полей
                                          # на списки ошибок для этих полей (поле может иметь более одной ошибки).
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])
