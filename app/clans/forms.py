from django import forms
from .models import Clan, Invite, Apply, Feature

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
    icon = forms.ImageField(required=False)
    # ここも改善
                            # widget=forms.Media(attrs={'class': 'form-control'}))
    url = forms.URLField(required=False,
                            widget=forms.URLInput(
                                attrs={'class': 'form-control', 'placeholder': 'クランの公式HPのURLを入力してください'}))
    description = forms.CharField(required=True,
                            widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'クランについての説明を入力してください'}))
    sponsor = forms.CharField(required=False,
                            widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'スポンサー名を入力してください'}))
    # 質問する
    # feature = forms.(required=True,
    #                         widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    desired_condition = forms.CharField(required=True,
                            widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': '募集する選手の希望条件を入力してください'}))
    disclosed = forms.BooleanField(required=True)


    def __init__(self, *args, **kwargs):
        super(ClanCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required':'{fieldname} は必須です。'.format(fieldname=field.label)}



class InviteCreateForm(forms.ModelForm):
    class Meta:
        model = Invite
        fields = ('message', 'invite_url')
        labels = {
            'message': 'メッセージ',
            'invite_url': '招待用URL',
        }

    message = forms.CharField(required=True,
                                widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': '招待理由を入力してください'}))
    invite_url = forms.URLField(required=True,
                                widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': '招待が承認された後に会話するDiscordのサーバー招待URLを入力してください'}))

    def __init__(self, *args, **kwargs):
        super(InviteCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required':'{fieldname} は必須です。'.format(fieldname=field.label)}



class ClanApplyCreateForm(forms.ModelForm):
    class Meta:
        model = Apply
        fields = ('message',)
        labels = {
            'message': '志望理由',
        }

    message = forms.CharField(required=True,
                                widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': '志望理由を入力してください'}))

    def __init__(self, *args, **kwargs):
        super(ClanApplyCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required':'{fieldname} は必須です。'.format(fieldname=field.label)}
