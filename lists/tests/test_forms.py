from django.test import TestCase
from ..forms import ItemForm, EMPTY_ITEM_ERROR
from ..models import Item, List

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

    def test_form_save_handles_saving_to_a_list(self):
        '''тест: метод save формы обрабатывает сохранение в список'''
        list_ = List.objects.create()
        form = ItemForm(data={'text': 'тест сохранения формой'})
        new_item = form.save(for_list=list_)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'тест сохранения формой')
        self.assertEqual(new_item.list, list_)
