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
    game_title = forms.ModelChoiceField(queryset=Game.objects.all(), required=False, empty_label='選択してください',
                            widget=forms.Select(attrs={'class': 'form-control'}))
    feature = forms.ModelChoiceField(queryset=Feature.objects.all(), empty_label='選択してください',
                            widget=forms.Select(attrs={'class': 'form-control'}))
    introduction = forms.CharField(required=False,
                            widget=forms.Textarea(attrs={'placeholder': '自身について入力してください', 'render_value': True}))
    clip_url = forms.URLField(required=False, widget=forms.URLInput())
    desired_job = forms.ModelChoiceField(queryset=Job.objects.all(), empty_label='希望するタイプを選択してください',
                            widget=forms.Select(attrs={'class': 'form-control'}), to_field_name="job")
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
