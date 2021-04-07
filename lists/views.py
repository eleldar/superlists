from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from .models import Item, List

def home_page(request):
    '''домашняя страница'''
    return render(request, 'lists/home.html')

def view_list(request, list_id):
    '''представление списка'''
    list_ = List.objects.get(id=list_id)
    error = None

    if request.method == 'POST':
        try:
            item = Item(text=request.POST['item_text'], list=list_)
            item.full_clean() # валидация модели из-за особенностей использования ORM с SQL
            item.save()
            return redirect(f'/lists/{list_.id}/')
        except ValidationError:
            error = 'Вы не можете вводить пустую строку!'
    context = {'list': list_, 'error': error}
    return render(request, 'lists/list.html', context=context)

def new_list(request):
    '''новый список'''
    list_ = List.objects.create()
    item = Item(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean() # валидация модели из-за особенностей использования ORM с SQL
        item.save()
    except ValidationError:
        list_.delete()
        error = 'Вы не можете вводить пустую строку!'
        return render(request, 'lists/home.html', {'error': error})
    return redirect(f'/lists/{list_.id}/')
