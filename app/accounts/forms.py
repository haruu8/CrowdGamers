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

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required':'{fieldname} は必須です。'.format(fieldname=field.label)}

            self.fields['name'].widget = forms.TextInput(
            attrs={
                'placeholder': '自身のニックネームを入力',
                'required': True,
                'class': 'form-control',
                }
            )
            # 画像は clearableFileInput でいいのか
            self.fields['icon'].widget = forms.ClearableFileInput(
                attrs={
                    'placeholder': 'アイコン',
                    'required': False,
                    'class': 'form-control',
                }
            )
            self.fields['twitter_url'].widget = forms.TextInput(
            attrs={
                'placeholder': '自身のTwitterのURLを入力してください。',
                'required': False,
                'class': 'form-control',
                }
            )
            self.fields['introduction'].widget = forms.TextInput(
            attrs={
                'placeholder': '自己紹介を入力してください。',
                'required': False,
                'class': 'form-control',
                }
            )
            self.fields['clip'].widget = forms.ClearableFileInput(
                attrs={
                    'placeholder': 'クリップ',
                    'required': False,
                    'class': 'form-control',
                }
            )
