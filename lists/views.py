from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item, List

def home_page(request):
    '''домашняя страница'''
    return render(request, 'lists/home.html')

def view_list(request):
    '''отображение нового списка'''
    items = Item.objects.all()
    return render(request, 'lists/list.html', {'items': items})

def new_list(request):
    '''новый список'''
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/uniq-list/')
