from django import forms
from .models import Item

EMPTY_ITEM_ERROR = 'Вы не можете вводить пустую строку!'

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
