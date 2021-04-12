from django import forms
from .models import Item
from django.core.exceptions import ValidationError

EMPTY_ITEM_ERROR = 'Вы не можете вводить пустую строку!'
DUPLICATE_ITEM_ERROR = 'У Вас уже есть этот элемент в списке'

class ItemForm(forms.models.ModelForm):
    '''форма для элемента списка'''
    def save(self, for_list):
        self.instance.list = for_list # Атрибут .instance на форме представляет объект базы данных, который модифицируется или создается
                                      # Есть другие способы заставить это работать, включая создание объекта вручную либо использование аргумента commit=False в функции save
        return super().save() # вызов метода модели

    class Meta:
        model = Item       # указываем, для какой модели предназначена форма
        fields = ('text',) # указываем какие поля мы хотим, чтобы она использовала
        widgets = {        # переопределение виджета, заполнителя и класса CSS
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Введите элемент списка',
                'class': 'form-control input-lg',
            }),
        }
        error_messages = { # определение собственного сообщения на ошибку валидации в форме (на основе модели)
            'text': {'required': EMPTY_ITEM_ERROR}
        }


class ExistingListItemForm(ItemForm):
    '''форма для элемента существующего списка'''

    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def validate_unique(self):
        '''проверка уникальности'''
        try:
            self.instance.validate_unique()
        except ValidationError as e:                        # берем ошибку валидации
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]} # корректируем ее сообщение
            self._update_errors(e)                          # передаем ее в форму.

    def save(self):
        return forms.models.ModelForm.save(self)
