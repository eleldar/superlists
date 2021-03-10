from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item

def home_page(request):
    '''домашняя страница'''
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text']) # создание нового объекта Item без необходимости вызывать метод .save()
        return redirect('/lists/uniq-list/')

    return render(request, 'lists/home.html')

def view_list(request):
    '''новый список'''
    items = Item.objects.all()
    return render(request, 'lists/list.html', {'items': items})

