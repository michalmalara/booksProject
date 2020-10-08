from django.db import models


# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=50, verbose_name='Tytuł')
    author = models.CharField(max_length=50, verbose_name='Autor')
    pub_date = models.DateField(verbose_name='Data publikacji')
    isbn = models.IntegerField(verbose_name='Numer ISBN')
    pages = models.IntegerField(verbose_name='Liczba stron')
    cover = models.URLField(verbose_name='Link do okładki')
    lang = models.CharField(max_length=10, verbose_name='Język')

    def __str__(self):
        return f'{self.title} - {self.author}'
