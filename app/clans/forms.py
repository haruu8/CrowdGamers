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

    name = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'クランの名前を入力してください'}))
    icon = forms.ImageField(required=False,
                            widget=forms.Media(attrs={'class': 'form-control'}))
    url = forms.URLField(required=False,
                            widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'クランの公式HPのURLを入力してください'}))
    description = forms.CharField(required=True,
                            widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'クランについての説明を入力してください'}))
    sponsor = forms.CharField(required=False,
                            widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'スポンサー名を入力してください'}))
    # 質問する
    feature = forms.(required=True,
                            widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    desired_condition = forms.CharField(required=True,
                            widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': '募集する選手の希望条件を入力してください'}))
    # クラス指定方法
    disclosed = forms.BooleanField(required=True, defalut=False)


    def __init__(self, *args, **kwargs):
        super(ClanCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required':'{fieldname} は必須です。'.format(fieldname=field.label)}
            # class の指定方法を調べる
            # field.class = 'form-control'



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
