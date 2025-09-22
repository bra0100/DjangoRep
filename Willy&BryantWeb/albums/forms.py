from django import forms
from .models import Album
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class AlbumForm(forms.ModelForm):
    
    release_day = forms.ChoiceField(
        choices=[(str(i).zfill(2), str(i)) for i in range(1, 32)])
    release_month = forms.ChoiceField(choices=[
        ('01', 'January'), ('02', 'February'), ('03', 'March'), ('04', 'April'),
        ('05', 'May'), ('06', 'June'), ('07', 'July'), ('08', 'August'),
        ('09', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')
    ])
    release_year = forms.ChoiceField(
        choices=[(str(i), str(i)) for i in range(1960, 2026)])

    class Meta:
        model = Album
        fields = ['band', 'title', 'genre', 'description', 'cover']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk and self.instance.release_date:
            self.fields['release_day'].initial = self.instance.release_date.strftime(
                '%d')
            self.fields['release_month'].initial = self.instance.release_date.strftime(
                '%m')
            self.fields['release_year'].initial = self.instance.release_date.strftime(
                '%Y')

    def save(self, commit=True, user=None):
        album = super().save(commit=False)
        if user:
            album.uploaded_by = user

       
        day = self.cleaned_data['release_day']
        month = self.cleaned_data['release_month']
        year = self.cleaned_data['release_year']
        album.release_date = f"{year}-{month}-{day}"

        if commit:
            album.save()

            if hasattr(self, 'save_m2m'):
                self.save_m2m()
        return album
