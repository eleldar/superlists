from django.db import models
from django.urls import reverse
from django.conf import settings

class List(models.Model):
    '''список'''
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        blank=True, null=True
    )

    def get_absolute_url(self):
        '''получить абсолютный url'''
        return reverse('view_list', args=[self.id])

    @staticmethod # необязателен!
    def create_new(first_item_text, owner=None):
        '''создать новый список'''
        list_ = List.objects.create(owner=owner)
        Item.objects.create(text=first_item_text, list=list_)
        return list_


class Item(models.Model):
    '''элемент списка'''
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)
        unique_together = ('list', 'text') # text и list должны быть уникальными вместе

    def __str__(self):
        return self.text
