from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item

def home_page(request):
    '''домашняя страница'''
    return render(request, 'lists/home.html')

def view_list(request):
    '''новый список'''
    items = Item.objects.all()
    return render(request, 'lists/list.html', {'items': items})

def new_list(request):
    '''новый список'''
    Item.objects.create(text=request.POST['item_text'])
    return redirect('/lists/uniq-list/')
