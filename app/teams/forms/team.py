from django import forms
from teams.models import Team, Game, Feature, Job



class TeamCreateForm(forms.ModelForm):
    """
    チームの作成・編集に使用するフォーム
    """
    class Meta:
        model = Team
        fields = ('teamname', 'name', 'icon', 'header', 'website', 'introduction',
                    'sponsor', 'game_title','feature', 'desired_job','desired_condition', 'disclosed')

    teamname = forms.CharField(required=True, label='チームネーム',
                            help_text='使用できるのは大文字・小文字アルファベット、数字、_(アンダーバー)のみです。',
                            widget=forms.TextInput(attrs={'placeholder': 'チームのユーザーネームを入力してください', 'render_value': True}))
    name = forms.CharField(required=True, label='名前',
                            widget=forms.TextInput(attrs={'placeholder': 'チームの名前を入力してください', 'render_value': True}))
    icon = forms.ImageField(required=False, label='アイコン')
    header = forms.ImageField(required=False, label='ヘッダー')
    website = forms.URLField(required=False, label='ウェブサイト',
                            widget=forms.URLInput(attrs={'placeholder': 'ウェブサイトのURLを入力してください', 'render_value': True}))
    introduction = forms.CharField(required=True, label='説明',
                            widget=forms.Textarea(attrs={'placeholder': 'チームについての概要を入力してください', 'render_value': True}))
    sponsor = forms.CharField(required=False,label='スポンサー',
                            widget=forms.Textarea(attrs={'placeholder': 'スポンサー名を入力してください', 'render_value': True}))
    game_title = forms.ModelMultipleChoiceField(queryset=Game.objects.all(), required=False, label='ゲームタイトル',
                            help_text='5つまで選択することができます。複数選択するときには Control キーを押したまま選択してください。Mac は Command キーを使ってください。',
                            widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    feature = forms.ModelMultipleChoiceField(queryset=Feature.objects.all(), label='特徴',
                            help_text='3つまで選択することができます。複数選択するときには Control キーを押したまま選択してください。Mac は Command キーを使ってください。',
                            widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    desired_job = forms.ModelMultipleChoiceField(queryset=Job.objects.all(), label='希望枠',
                            help_text='3つまで選択することができます。複数選択するときには Control キーを押したまま選択してください。Mac は Command キーを使ってください。',
                            widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    desired_condition = forms.CharField(required=False, label='希望条件',
                            widget=forms.Textarea(attrs={'placeholder': '募集する選手の希望条件を入力してください', 'render_value': True}))
    disclosed = forms.BooleanField(required=False, label='公開・非公開')

    def __init__(self, *args, **kwargs):
        """
        一括でエラーメッセージを設定する
        """
        super(TeamCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required':'{fieldname} は必須です。'.format(fieldname=field.label)}
            field.widget.attrs['class'] = 'form-control'

    def clean_teamname(self):
        """
        teamname の文字数制限を設定する。
        """
        teamname = self.cleaned_data['teamname']
        if len(teamname) <= 3 or len(teamname) >= 16:
            raise forms.ValidationError('チームネームは4~15字で設定してください')
        return teamname

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
        desired_job の選択上限を3つに設定する。
        """
        desired_job = self.cleaned_data['desired_job']
        if len(desired_job) >= 4:
            raise forms.ValidationError('希望枠は3つまでしか選択することができません')
        return desired_job
