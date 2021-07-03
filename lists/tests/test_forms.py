import unittest
from unittest.mock import patch, Mock
from django.test import TestCase
from ..models import Item, List
from ..forms import (
    DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR,
    ExistingListItemForm, ItemForm, NewListForm
)

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

class NewListFormTest(unittest.TestCase):
    '''тест формы для нового списка'''

    @patch('lists.forms.List.create_new') # имитируем класс List из уровня модели
    def test_save_creates_new_list_from_post_data_if_user_authenticated(
        self, mock_List_create_new
    ):
        '''тест: save создает новый список из POST-запроса,
           если пользователь не аутентифицирован'''
        user = Mock(is_authenticated=False)
        form = NewListForm(data={'text': 'Новый элемент списка'})
        form.is_valid() # чтобы форма заполнила словарь cleaned_data, где она хранит проверенные данные
        form.save(owner=user)
        mock_List_create_new.assert_called_once_with(
            first_item_text = 'Новый элемент списка'
        )

    @patch('lists.forms.List.create_new')
    def test_save_creates_new_list_with_owner_if_user_authenticated(
        self, mock_List_create_new
    ):
        '''тест: save создает новый список с владельцем,
           если пользователь аутентифицирован'''
        user = Mock(is_authenticated=True)
        form = NewListForm(data={'text': 'Новый элемент списка'})
        form.is_valid() # чтобы форма заполнила словарь cleaned_data, где она хранит проверен>
        form.save(owner=user)
        mock_List_create_new.assert_called_once_with(
            first_item_text = 'Новый элемент списка', owner=user
        )

