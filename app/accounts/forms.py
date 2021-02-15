from django import forms
from .models import User



class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username',)
        labels = {
            'username': 'ユーザーネーム',
        }

    username = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'placeholder': 'ユーザーネームを入力してください', 'render_value': True}))

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required':'{fieldname} は必須です。'.format(fieldname=field.label)}
            field.widget.attrs['class'] = 'form-control'
