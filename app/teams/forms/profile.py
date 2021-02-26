from django import forms
from teams.models import UserProfile, Game, Feature



class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('name', 'icon', 'header', 'game_title', 'feature', 'introduction', 'clip_url')
        labels = {
            'name': '名前',
            'icon': 'アイコン',
            'header': 'ヘッダー画像',
            'game_title': 'ゲームタイトル',
            'feature': '特徴',
            'introduction': '自己紹介',
            'clip_url': 'クリップ',
        }

    JOB_TYPE = (
        (1, '選手'),
        (2, 'マネージャー'),
        (3, 'コーチ'),
    )

    name = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'placeholder': '名前を入力してください', 'render_value': True}))
    icon = forms.ImageField(required=False)
    header = forms.ImageField(required=False)
    game_title = forms.ModelChoiceField(queryset=Game.objects.all(), required=False, empty_label='選択してください',
                            widget=forms.Select(attrs={'class': 'form-control'}))
    feature = forms.ModelChoiceField(queryset=Feature.objects.all(), empty_label='選択してください',
                            widget=forms.Select(attrs={'class': 'form-control'}))
    introduction = forms.CharField(required=False,
                            widget=forms.Textarea(attrs={'placeholder': '自身について入力してください', 'render_value': True}))
    clip_url = forms.URLField(required=False, widget=forms.URLInput())
    desired_job_type = forms.CharField(required=True,
                            widget=forms.Select(choices=JOB_TYPE, attrs={'class': 'form-control'}))

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
