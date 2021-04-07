from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models import Item, List


class ListAndItemModelTest(TestCase):
    '''тест модели списка и элемента списка'''
    def test_saving_and_retrieving_items(self):
        '''тест сохранения и получения элементов списка'''
        list_ = List() # cоздаем новый объект List и назначаем ему каждый элемент
        list_.save()

        first_item = Item()
        first_item.text = 'Первый (какой-нибудь) элемент списка'
        first_item.list = list_ # присваиваем свойству list
        first_item.save()

        second_item = Item()
        second_item.text = 'Второй элемент списка'
        second_item.list = list_ # присваиваем свойству list
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_) # проверяем, что список должным образом сохранен

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'Первый (какой-нибудь) элемент списка')
        self.assertEqual(first_saved_item.list, list_) # проверяем, что первый элемент сохранил связь со списком сохранен
        self.assertEqual(second_saved_item.text, 'Второй элемент списка')
        self.assertEqual(second_saved_item.list, list_)  # проверяем, что второй элемент сохранил связь со списком

    def test_cannot_save_empty_list_items(self):
        '''тест: нельзя добавлять пустые элементы списка'''
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError): # использование менеджера контекста для генерации ошибки в случае невозможности сохранить пустой элемент списка
            item.save()
            item.full_clean() # метод ручного выполнения полной валидации

    def test_get_absolute_url(self):
        '''тест: получение абсолютного URL'''
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')
