from django import forms
from .models import User



class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('name', 'icon', 'age', 'twitter_url', 'introduction', 'clip')
        labels = {
            'name': '名前',
            'icon': 'アイコン',
            'age': '年齢',
            'twitter_url': 'TwitterのURL',
            'introduction': '自己紹介',
            'clip': 'クリップ'
        }

    name = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'placeholder': '名前を入力してください', 'render_value': True}))
    icon = forms.ImageField(required=False)
    twitter_url = forms.URLField(required=False,
                            widget=forms.URLInput(attrs={'placeholder': 'TwitterのURLを入力してください', 'render_value': True}))
    introduction = forms.CharField(required=False,
                            widget=forms.Textarea(attrs={'placeholder': '自身について入力してください', 'render_value': True}))
    clip = forms.FileField(required=False,
                            widget=forms.ClearableFileInput())

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required':'{fieldname} は必須です。'.format(fieldname=field.label)}
            field.widget.attrs['class'] = 'form-control'
