from django.test import TestCase
from ..forms import ItemForm, ExistingListItemForm, EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR
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

class ExistingListFormTest(TestCase):
    '''тест формы элемента существуюущего списка'''

    def test_form_renders_item_text_input(self):
        '''тест: форма отображает текстовый ввод элемента'''
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_)
        self.assertIn('placeholder="Введите элемент списка"', form.as_p())

    def test_form_validation_for_blank_items(self):
        '''тест: валидация формы для пустых элементов'''
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_validation_for_duplicate_items(self):
        '''тест: валидация формы для повторных элементов'''
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='нет дубликатов!')
        form = ExistingListItemForm(for_list=list_, data={'text': 'нет дубликатов!'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])

    def test_form_save(self):
        '''тест сохранения формы'''
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': 'сохранение'})
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.all()[0])
