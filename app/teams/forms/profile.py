from django import forms
from teams.models import UserProfile, Game, Feature, Job



class UserProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('name', 'icon', 'header', 'game_title', 'feature',
                    'introduction', 'clip_url', 'desired_job', 'desired_condition', 'disclosed')
        labels = {
            'name': '名前',
            'icon': 'アイコン',
            'header': 'ヘッダー画像',
            'game_title': 'ゲームタイトル',
            'feature': '特徴',
            'introduction': '自己紹介',
            'clip_url': 'クリップ',
            'desired_job': '希望職',
            'desired_condition': '希望条件',
            'disclosed': '公開・非公開',
        }

    name = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'placeholder': '名前を入力してください', 'render_value': True}))
    icon = forms.ImageField(required=False)
    header = forms.ImageField(required=False)
    introduction = forms.CharField(required=False,
                            widget=forms.Textarea(attrs={'placeholder': '自身について入力してください', 'render_value': True}))
    clip_url = forms.URLField(required=False, help_text='埋め込みURLは普通のリンクとは違います！設定方法は<a href="https://support.google.com/youtube/answer/171780?hl=ja" target="_blank">こちら</a>からご確認ください。(リンクのみを貼り付けください)',
                            widget=forms.URLInput())
    game_title = forms.ModelMultipleChoiceField(queryset=Game.objects.all(), required=True, help_text='5つまで選択することができます。複数選択するときには Control キーを押したまま選択してください。Mac は Command キーを使ってください。',
                            widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    feature = forms.ModelMultipleChoiceField(queryset=Feature.objects.all(), required=True, help_text='3つまで選択することができます。複数選択するときには Control キーを押したまま選択してください。Mac は Command キーを使ってください。',
                            widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    desired_job = forms.ModelMultipleChoiceField(queryset=Job.objects.all(), required=True, help_text='1つまで選択することができます',
                            widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    desired_condition = forms.CharField(required=False,
                            widget=forms.Textarea(attrs={'placeholder': '募集する選手の希望条件を入力してください', 'render_value': True}))
    disclosed = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(UserProfileUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required':'{fieldname} は必須です。'.format(fieldname=field.label)}
            field.widget.attrs['class'] = 'form-control'

    # 特徴を三つまでしか選択できないようにする validation
    def clean_feature(self):
        feature = self.cleaned_data['feature']
        if len(feature) >= 4:
            raise forms.ValidationError('特徴は3つまでしか選択することができません')
        return feature

    # ゲームタイトルを五つまでしか選択できないようにする validation
    def clean_game_title(self):
        game_title = self.cleaned_data['game_title']
        if len(game_title) >= 6:
            raise forms.ValidationError('ゲームタイトルは5つまでしか選択することができません')
        return game_title

    # 希望職を1つまでしか選択できないようにする validation
    def clean_desired_job(self):
        desired_job = self.cleaned_data['desired_job']
        if len(desired_job) >= 2:
            raise forms.ValidationError('希望職は1つまでしか選択することができません')
        return desired_job
