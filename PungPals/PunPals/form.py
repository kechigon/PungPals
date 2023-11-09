from django import forms
from django.contrib.auth import get_user_model


from .models import CustomUser, Room

class SignUpForm(forms.Form):
    username = forms.CharField(label='ユーザー名', max_length=100)
    password1 = forms.CharField(label='パスワード', widget=forms.PasswordInput)
    password2 = forms.CharField(label='パスワード（確認用）', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('パスワードが一致しません')
        
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('既に存在するユーザー名です')
        
class RoomCountCleanMixin:
    def clean(self):
        super().clean()

        user = get_user_model().objects.get(username=self.request.user.username)

        if user.room_set.count() >= 10:
            raise forms.ValidationError("所属できる部屋数の上限に達しています")
        
class CreateRoomForm(RoomCountCleanMixin, forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'passwd']
        labels = {'name': '部屋名',
                  'passwd': 'パスワード'
                  }
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['maxlength'] = 100
        
class JoinRoomForm(RoomCountCleanMixin, forms.Form):
    roomname = forms.CharField(label='部屋名', max_length=100)
    password = forms.CharField(label='パスワード')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)