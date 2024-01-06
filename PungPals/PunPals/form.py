from django import forms
from django.contrib.auth import get_user_model


from .models import CustomUser, Room, Taikyoku3, Taikyoku4

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

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Room.objects.filter(name=name).exists():
            raise forms.ValidationError("既に存在する部屋名です")
        return name
        
class JoinRoomForm(RoomCountCleanMixin, forms.Form):
    roomname = forms.CharField(label='部屋名', max_length=100)
    password = forms.CharField(label='パスワード')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

class Taikyoku3Form(forms.ModelForm):

    class Meta:
        model = Taikyoku3
        fields = ['userTon', 'tonScore', 'userNan', 'nanScore', 'userSya', 'syaScore']

    def __init__(self, *args, **kwargs):
        roomname = kwargs.pop('roomname')
        super(Taikyoku3Form, self).__init__(*args, **kwargs)
        room = Room.objects.get(name=roomname)
        self.fields['userTon'].queryset = room.users.all()
        self.fields['userNan'].queryset = room.users.all()
        self.fields['userSya'].queryset = room.users.all()

        self.fields['userTon'].label = '東'
        self.fields['tonScore'].label = '東の得点'
        self.fields['userNan'].label = '南'
        self.fields['nanScore'].label = '南の得点'
        self.fields['userSya'].label = '西'
        self.fields['syaScore'].label = '西の得点'

class Taikyoku4Form(forms.ModelForm):

    class Meta:
        model = Taikyoku4
        fields = ['userTon', 'tonScore', 'userNan', 'nanScore', 'userSya', 'syaScore', 'userPe', 'peScore']

    def __init__(self, *args, **kwargs):
        roomname = kwargs.pop('roomname')
        super(Taikyoku4Form, self).__init__(*args, **kwargs)
        room = Room.objects.get(name=roomname)
        self.fields['userTon'].queryset = room.users.all()
        self.fields['userNan'].queryset = room.users.all()
        self.fields['userSya'].queryset = room.users.all()
        self.fields['userPe'].queryset = room.users.all()

        self.fields['userTon'].label = '東'
        self.fields['tonScore'].label = '東の得点'
        self.fields['userNan'].label = '南'
        self.fields['nanScore'].label = '南の得点'
        self.fields['userSya'].label = '西'
        self.fields['syaScore'].label = '西の得点'
        self.fields['userPe'].label = '北'
        self.fields['peScore'].label = '北の得点'

GAME_CHOICES = [
    ('senseki3', '三麻'),
    ('senseki4', '四麻'),
]

SORT_CHOICES = [
    ('rankMean', '平均順位'),
    ('firstRate', '一着率'),
    ('secondRate', '二着率'),
    ('thirdRate', '三着率'),
    ('fourthRate', '四着率'),
    ('outRate', '飛び率'),
    ('gameNum', '局数'),
    ('scoreMean', '平均スコア'),
]

class RankingFilterForm(forms.Form):
    game_type = forms.ChoiceField(choices=GAME_CHOICES, label='ゲームタイプ')
    game_num = forms.IntegerField(min_value=1, label='最低局数')
    sort_by = forms.ChoiceField(choices=SORT_CHOICES, label='項目')