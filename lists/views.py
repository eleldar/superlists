from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from .models import Item, List
from .forms import ItemForm, ExistingListItemForm, NewListForm
from django.contrib.auth import get_user_model
User = get_user_model()

def home_page(request):
    '''домашняя страница'''
    context = {'form': ItemForm()}
    return render(request, 'lists/home.html', context=context)

def view_list(request, list_id):
    '''представление списка'''
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_) # за кадром используется get_absolute_url
    context = {'list': list_, 'form': form}
    return render(request, 'lists/list.html', context=context)

def new_list(request):
    '''новый список'''
    form = ItemForm(data=request.POST) # передаем данные POST-запроса в конструктор формы
    if form.is_valid(): # проверяем на допустимость введенных данных
        list_ = List()
        if request.user.is_authenticated:
            list_.owner = request.user
        list_.save()
        form.save(for_list=list_)
        return redirect(str(list_.get_absolute_url()))
    else:
        # Если введенное значение недопустимое, передаем форму в шаблон вместо
        # жестко кодированного строкового значения ошибки
        context = {'form': form}
        return render(request, 'lists/home.html', context=context)

def new_list2(request):
    '''новый список 2'''
    form = NewListForm(data=request.POST)
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(str(list_))
    return render(request, 'lists/home.html', {'form': form})

def my_lists(request, email):
    '''мои списки'''
    owner = User.objects.get(email=email)
    context = {'owner': owner}
    return render(request, 'lists/my_lists.html', context=context)
