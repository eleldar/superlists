from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from .models import Item, List
from .forms import ItemForm

def home_page(request):
    '''домашняя страница'''
    context = {'form': ItemForm()}
    return render(request, 'lists/home.html', context=context)

def view_list(request, list_id):
    '''представление списка'''
    list_ = List.objects.get(id=list_id)
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            form.save(for_list=list_)
            return redirect(list_) # за кадром используется get_absolute_url
    context = {'list': list_, 'form': form}
    return render(request, 'lists/list.html', context=context)

def new_list(request):
    '''новый список'''
    form = ItemForm(data=request.POST) # передаем данные POST-запроса в конструктор формы
    if form.is_valid(): # проверяем на допустимость введенных данных
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        # Если введенное значение недопустимое, передаем форму в шаблон вместо
        # жестко кодированного строкового значения ошибки
        context = {'form': form}
        return render(request, 'lists/home.html', context=context)
