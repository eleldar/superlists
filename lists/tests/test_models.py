from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models import Item, List


class ItemModelTest(TestCase):
    '''тест модели элемента списка'''
    def test_default_text(self):
        '''тест текста, заданного по умолчанию'''
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        '''тест: элемент связан со списком'''
        list_ = List.objects.create() 
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_cannot_save_empty_list_items(self):
        '''тест: нельзя добавлять пустые элементы списка'''
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError): # использование менеджера контекста для генерации ошибки в случае невозможности сохранить пустой элемент списка
            item.save()
            item.full_clean() # метод ручного выполнения полной валидации

    def test_string_representation(self):
        '''тест строкового представления'''
        item = Item(text='Тест строки')
        self.assertEqual(str(item), 'Тест строки')

    def test_duplicate_items_are_invalid(self):
        '''тест: повторы элементов недопустимы'''
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='Текст для проверки повтора')
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='Текст для проверки повтора')
            item.full_clean()


    def test_can_save_same_item_to_different_lists(self):
        '''тест: может сохранять этот же элемент в разные списки'''
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='Текст для проверки повтора')
        item = Item(list=list2, text='Текст для проверки повтора')
        item.full_clean() # не должен поднять исключение, т.к. это другой список


class ListModelTest(TestCase):
    '''тест модели списка'''
    def test_get_absolute_url(self):
        '''тест: получение абсолютного URL'''
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')

    def test_list_ordering(self):
        '''тест упорядочения списка'''
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='i1')
        item2 = Item.objects.create(list=list1, text='i2')
        item3 = Item.objects.create(list=list1, text='i3')
        self.assertEqual(
            list(Item.objects.all()),
            [item1, item2, item3]
        )
