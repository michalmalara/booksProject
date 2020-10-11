from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=50, verbose_name='Tytuł')
    author = models.CharField(max_length=50, verbose_name='Autor')
    pub_date = models.DateField(verbose_name='Data publikacji')
    # isbn = models.IntegerField(verbose_name='Numer ISBN', blank=True,
    #                            validators=[MinValueValidator(1000000000000), MaxValueValidator(9999999999999)])
    isbn = models.CharField(max_length=13, verbose_name='Numer ISBN', validators=[MinLengthValidator(10)])
    pages = models.IntegerField(verbose_name='Liczba stron')
    cover = models.URLField(verbose_name='Link do okładki', blank=True)
    lang = models.CharField(max_length=2, verbose_name='Język')

    def __str__(self):
        return f'{self.title} - {self.author}'

    def save(self, *args, **kwargs):
        self.lang = self.lang.upper()
        return super(Book, self).save(*args, **kwargs)


