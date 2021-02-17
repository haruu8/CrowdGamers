from django import forms
from .models import Team, Invite, Apply, Feature, UserProfile



class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('name', 'icon', 'header', 'date_of_birth', 'introduction', 'clip_url')
        labels = {
            'name': '名前',
            'icon': 'アイコン',
            'header': 'ヘッダー画像',
            'date_of_birth': '生年月日',
            'introduction': '自己紹介',
            'clip_url': 'クリップ',
        }
    name = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'placeholder': '名前を入力してください', 'render_value': True}))
    icon = forms.ImageField(required=False)
    header = forms.ImageField(required=False)
    date_of_birth = forms.DateField(required=True,
                            widget=forms.SelectDateWidget())
    introduction = forms.CharField(required=False,
                            widget=forms.Textarea(attrs={'placeholder': '自身について入力してください', 'render_value': True}))
    clip_url = forms.URLField(required=False, widget=forms.URLInput())

    def __init__(self, *args, **kwargs):
        super(UserProfileUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required':'{fieldname} は必須です。'.format(fieldname=field.label)}
            field.widget.attrs['class'] = 'form-control'



class TeamCreateForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = ('teamname', 'name', 'icon', 'url', 'description',
                    'sponsor', 'feature', 'desired_condition', 'disclosed')
        labels = {
            'teamname': 'チームネーム',
            'name': '名前',
            'icon': 'アイコン',
            'url': '公式のURL',
            'description': '説明',
            'sponsor': 'スポンサー',
            'feature': '特徴',
            'desired_condition': '希望条件',
            'disclosed': '公開・非公開',
        }

    teamname = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'placeholder': 'チームのユーザーネームを入力してください', 'render_value': True}))
    name = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'placeholder': 'クランの名前を入力してください', 'render_value': True}))
    icon = forms.ImageField(required=False)
    url = forms.URLField(required=False,
                            widget=forms.URLInput(attrs={'placeholder': 'クランの公式HPのURLを入力してください', 'render_value': True}))
    description = forms.CharField(required=True,
                            widget=forms.Textarea(attrs={'placeholder': 'クランについて入力してください', 'render_value': True}))
    sponsor = forms.CharField(required=False,
                            widget=forms.Textarea(attrs={'placeholder': 'スポンサー名を入力してください', 'render_value': True}))
    feature = forms.MultipleChoiceField(required=False,
                            widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}))
    desired_condition = forms.CharField(required=True,
                            widget=forms.Textarea(attrs={'placeholder': '募集する選手の希望条件を入力してください', 'render_value': True}))
    disclosed = forms.BooleanField(required=True)


    def __init__(self, *args, **kwargs):
        super(TeamCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required':'{fieldname} は必須です。'.format(fieldname=field.label)}
            field.widget.attrs['class'] = 'form-control'



class UserInviteCreateForm(forms.ModelForm):
    class Meta:
        model = Invite
        fields = ('message', 'invite_url')
        labels = {
            'message': 'メッセージ',
            'invite_url': '招待用URL',
        }

    message = forms.CharField(required=True,
                                widget=forms.Textarea(attrs={'placeholder': '招待理由を入力してください', 'render_value': True}))
    invite_url = forms.URLField(required=True,
                                widget=forms.URLInput(attrs={'placeholder': '招待が承認された後に会話するDiscordのサーバー招待URLを入力してください', 'render_value': True}))

    def __init__(self, *args, **kwargs):
        super(UserInviteCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required':'{fieldname} は必須です。'.format(fieldname=field.label)}
            field.widget.attrs['class'] = 'form-control'



class TeamApplyCreateForm(forms.ModelForm):
    class Meta:
        model = Apply
        fields = ('message',)
        labels = {
            'message': '志望理由',
        }

    message = forms.CharField(required=True,
                                widget=forms.Textarea(attrs={'placeholder': '志望理由を入力してください', 'render_value': True}))

    def __init__(self, *args, **kwargs):
        super(TeamApplyCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required':'{fieldname} は必須です。'.format(fieldname=field.label)}
            field.widget.attrs['class'] = 'form-control'
