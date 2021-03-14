from django import forms
from teams.models import UserProfile, Game, Feature, Job



class UserProfileUpdateForm(forms.ModelForm):
    """
    ユーザープロフィールを編集するフォーム。
    """
    class Meta:
        model = UserProfile
        fields = ('name', 'icon', 'header', 'game_title', 'feature',
                    'introduction', 'website', 'clip_url', 'desired_job', 'desired_condition', 'disclosed')

    name = forms.CharField(required=True, label='名前',
                            help_text='使用できるのは大文字・小文字アルファベット、数字、_(アンダーバー)のみです。',
                            widget=forms.TextInput(attrs={'placeholder': '名前を入力してください', 'render_value': True}))
    icon = forms.ImageField(required=False, label='アイコン')
    header = forms.ImageField(required=False, label='ヘッダー')
    introduction = forms.CharField(required=False, label='説明',
                            widget=forms.Textarea(attrs={'placeholder': '自身について入力してください', 'render_value': True}))
    website = forms.URLField(required=False, label='ウェブサイト',
                            help_text='ウェブサイトのリンクを入力してください',
                            widget=forms.URLInput())
    clip_url = forms.URLField(required=False, label='クリップ', help_text='埋め込みURLは普通のリンクとは違います！設定方法は<a href="https://support.google.com/youtube/answer/171780?hl=ja" target="_blank">こちら</a>からご確認ください。(リンクのみを貼り付けください)',
                            widget=forms.URLInput())
    game_title = forms.ModelMultipleChoiceField(queryset=Game.objects.all(), required=True, label='ゲームタイトル',
                            help_text='5つまで選択することができます。複数選択するときには Control キーを押したまま選択してください。Mac は Command キーを使ってください。',
                            widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    feature = forms.ModelMultipleChoiceField(queryset=Feature.objects.all(), required=True, label='特徴',
                            help_text='3つまで選択することができます。複数選択するときには Control キーを押したまま選択してください。Mac は Command キーを使ってください。',
                            widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    desired_job = forms.ModelMultipleChoiceField(queryset=Job.objects.all(), required=True, label='希望枠',
                            help_text='1つまで選択することができます',
                            widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    desired_condition = forms.CharField(required=False, label='希望条件',
                            widget=forms.Textarea(attrs={'placeholder': '募集する選手の希望条件を入力してください', 'render_value': True}))
    disclosed = forms.BooleanField(required=False, label='公開・非公開')

    def __init__(self, *args, **kwargs):
        """
        一括でエラーメッセージを設定する。
        """
        super(UserProfileUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required':'{fieldname} は必須です。'.format(fieldname=field.label)}
            field.widget.attrs['class'] = 'form-control'

    def clean_feature(self):
        """
        feature の選択上限を3つに設定する。
        """
        feature = self.cleaned_data['feature']
        if len(feature) >= 4:
            raise forms.ValidationError('特徴は3つまでしか選択することができません')
        return feature

    def clean_game_title(self):
        """
        game_title の選択上限を5つに設定する。
        """
        game_title = self.cleaned_data['game_title']
        if len(game_title) >= 6:
            raise forms.ValidationError('ゲームタイトルは5つまでしか選択することができません')
        return game_title

    def clean_desired_job(self):
        """
        desired_job の選択上限を1つに設定する。
        """
        desired_job = self.cleaned_data['desired_job']
        if len(desired_job) >= 2:
            raise forms.ValidationError('希望枠は1つまでしか選択することができません')
        return desired_job
