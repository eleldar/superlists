from django.db import models
from django.urls import reverse

# Create your models here.

class List(models.Model):
    '''список'''

    def get_absolute_url(self):
        '''получить абсолютный url'''
        return reverse('view_list', args=[self.id])

    def create_new():
        '''создать новый'''
        pass


class Item(models.Model):
    '''элемент списка'''
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)
        unique_together = ('list', 'text') # text и list должны быть уникальными вместе

    def __str__(self):
        return self.text
