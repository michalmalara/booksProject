from django import forms

DIRECTION = (
    ('ASC', 'rosnąco'),
    ('DESC', 'malejąco')
)


class BooksSearchForm(forms.Form):
    title = forms.CharField(max_length=50, label='Tytuł')
    author = forms.CharField(max_length=50, label='Autor')
    isbn = forms.IntegerField(label='Numer ISBN')
    lang = forms.CharField(max_length=10, label='Język')

    SORTING = ('title', 'author', 'pub_date', 'isbn', 'pages', 'lang')
    SORTING_NAMES = ('Tytuł', 'Autor', 'Data publikacji', 'Numer ISBN', 'Liczba stron', 'Język')
    sorting = forms.ChoiceField(choices=[('', '')] + list(zip(SORTING, SORTING_NAMES)), label='Sortuj po')
    sorting_direction = forms.ChoiceField(choices=DIRECTION, label='Kierunek sortowania')

    published_starting_date = forms.DateField(label='Opublikowano po dniu')
    published_ending_date = forms.DateField(label='Opublikowano przed dniem')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].required = False


