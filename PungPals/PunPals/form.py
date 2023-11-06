from django import forms
from .models import CustomUser

class SignUpForm(forms.Form):
    username = forms.CharField(label='ユーザー名', max_length=100)
    password1 = forms.CharField(label='パスワード', widget=forms.PasswordInput)
    password2 = forms.CharField(label='パスワード（確認用）', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('パスワードが一致しません')
        
        if CustomUser.objects.get(username=username):
            raise forms.ValidationError('既に存在するユーザー名です')