from django import forms

class ItemForm(forms.Form):
    '''форма для элемента списка'''
    item_text = forms.CharField(
        widget=forms.fields.TextInput(attrs={
            'placeholder': 'Введите элемент списка',
            'class': 'form-control input-lg',
        }),
    )
