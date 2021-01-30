from django import forms
from .models import Clan, Invite, Apply

class ClanCreateForm(forms.ModelForm):

    class Meta:
        model = Clan
        fields = ('name', 'icon', 'url', 'description',
                    'sponsor', 'feature', 'desired_condition', 'disclosed')
        labels = {
            'name': '名前',
            'icon': 'アイコン',
            'url': '公式のURL',
            'description': '説明',
            'sponsor': 'スポンサー',
            'feature': '特徴',
            'desired_condition': '希望条件',
            'disclosed': '公開・非公開',
        }

    def __init__(self, *args, **kwargs):
        super(ClanCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required':'{fieldname} は必須です。'.format(fieldname=field.label)}

        self.fields['name'].widget = forms.TextInput(
            attrs={
                'placeholder': 'クランの名前を入力してください',
                'required': True,
                'class': 'form-control',
            }
        )
        # 画像は clearableFileInput でいいのか
        self.fields['icon'].widget = forms.ClearableFileInput(
            attrs={
                'placeholder': 'アイコン',
                'required': True,
                'class': 'form-control',
            }
        )
        # TextInput でいいのか
        self.fields['url'].widget = forms.TextInput(
            attrs={
                'placeholder': 'クランの公式HPのURLを表示してください',
                'required': True,
                'class': 'form-control',
            }
        )
        self.fields['description'].widget = forms.TextInput(
            attrs={
                'placeholder': 'クランについての説明を記入ください。',
                'required': True,
                'class': 'form-control',
            }
        )
        self.fields['sponsor'].widget = forms.TextInput(
            attrs={
                'placeholder': 'スポンサーがいる場合は、スポンサー名を入力してください。',
                'required': True,
                'class': 'form-control',
            }
        )
        # TextInput でいいのか
        self.fields['feature'].widget = forms.TextInput(
            attrs={
                'placeholder': 'クランの特徴を選択してください。',
                'required': True,
                'class': 'form-control',
            }
        )
        self.fields['desired_condition'].widget = forms.TextInput(
            attrs={
                'placeholder': '募集する選手の希望条件を記入して下さい。',
                'required': True,
                'class': 'form-control',
            }
        )
        # TextInput でいいのか
        self.fields['disclosed'].widget = forms.TextInput(
            attrs={
                'placeholder': '希望条件の公開・非公開を選択してください。',
                'required': True,
                'class': 'form-control',
            }
        )



class InviteCreateForm(forms.ModelForm):

    class Meta:
        model = Invite
        fields = ('message', 'invite_url')
        labels = {
            'message': 'メッセージ',
            'invite_url': '招待用URL',
        }

    def __init__(self, *args, **kwargs):
        super(InviteCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required':'{fieldname} は必須です。'.format(fieldname=field.label)}

        self.fields['message'].widget = forms.TextInput(
            attrs={
                'placeholder': '招待された方が見る内容です。',
                'required': False,
                'class': 'form-control',
            }
        )
        self.fields['invite_url'].widget = forms.TextInput(
            attrs={
                'placeholder': '招待が承認されたら、確認することのできるURLです。Discordの仮入隊用URLなどが良いかもしれません。',
                'required': True,
                'class': 'form-control',
            }
        )



class ClanApplyCreateForm(forms.ModelForm):
    class Meta:
        model = Apply
        fields = ('message', 'achievement')
        labels = {
            'message': '志望理由',
            'achievement': '実績',
        }

    def __init__(self, *args, **kwargs):
        super(ClanApplyCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required':'{fieldname} は必須です。'.format(fieldname=field.label)}
        self.fields['message'].widget = forms.TextInput(
            attrs={
                'placeholder': '志望理由についてお書きください。また、仮入隊時に伝えたいことなどもありましたらお書きください。',
                'required': True,
                'class': 'form-control',
            }
        )
        self.fields['achievement'].widget = forms.TextInput(
            attrs={
                'placeholder': '実績や、自己PRをお書きください。',
                'required': True,
                'class': 'form-control',
            }
        )
