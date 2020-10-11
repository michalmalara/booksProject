from django import forms

class BooksSearchForm(forms.Form):
    title = forms.CharField(max_length=50, label='Tytuł')
    author = forms.CharField(max_length=50, label='Autor')
    isbn = forms.CharField(max_length=13, label='Numer ISBN')
    lang = forms.CharField(max_length=10, label='Język')

    published_starting_date = forms.DateField(label='Opublikowano po dniu')
    published_ending_date = forms.DateField(label='Opublikowano przed dniem')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].required = False


class ImportBooksForm(forms.Form):
    intitle = forms.CharField(max_length=50, label='Tytuł')
    inauthor = forms.CharField(max_length=50, label='Autor')
    inpublisher = forms.CharField(max_length=50, label='Wydawca')
    subject = forms.CharField(max_length=50, label='Temat')
    isbn = forms.IntegerField(label='ISBN')
    lccn = forms.IntegerField(label='LCCN')
    oclc = forms.IntegerField(label='OCLC')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].required = False