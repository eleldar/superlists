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
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'], list=list_)
        return redirect(f'/lists/{list_.id}/')
    return render(request, 'lists/list.html', {'list': list_})

def new_list(request):
    '''новый список'''
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list=list_) # создаем новый список для каждой отдельной записи (при отправки POST-запроса), ПОКА!
    try:
        item.full_clean() # валидация модели
        item.save()
    except ValidationError:
        list_.delete()
        error = 'Вы не можете вводить пустую строку!'
        return render(request, 'lists/home.html', {'error': error})
    return redirect(f'/lists/{list_.id}/')
