from django import forms
from django.contrib.auth.forms import UserCreationForm
from account.models import User, UserManager

class RegistarationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def save(self, commit = True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["username"]+"@email.com"
        if commit:
            user.save()
        return user
