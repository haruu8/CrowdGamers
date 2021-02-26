from django import forms
from teams.models import Team, Game, Feature



class TeamCreateForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = ('teamname', 'name', 'icon', 'header', 'url', 'description',
                    'sponsor', 'game_title','feature', 'desired_condition', 'disclosed')
        labels = {
            'teamname': 'チームネーム',
            'name': '名前',
            'icon': 'アイコン',
            'header': 'ヘッダー',
            'url': '公式のURL',
            'description': '説明',
            'sponsor': 'スポンサー',
            'game': 'ゲームタイトル',
            'feature': '特徴',
            'desired_condition': '希望条件',
            'disclosed': '公開・非公開',
        }

    teamname = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'placeholder': 'チームのユーザーネームを入力してください', 'render_value': True}))
    name = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'placeholder': 'チームの名前を入力してください', 'render_value': True}))
    icon = forms.ImageField(required=False)
    header = forms.ImageField(required=False)
    url = forms.URLField(required=False,
                            widget=forms.URLInput(attrs={'placeholder': 'チームの公式HPのURLを入力してください', 'render_value': True}))
    description = forms.CharField(required=True,
                            widget=forms.Textarea(attrs={'placeholder': 'チームについて入力してください', 'render_value': True}))
    sponsor = forms.CharField(required=False,
                            widget=forms.Textarea(attrs={'placeholder': 'スポンサー名を入力してください', 'render_value': True}))
    game_title = forms.ModelMultipleChoiceField(queryset=Game.objects.all(), required=False,
                            widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    feature = forms.ModelMultipleChoiceField(queryset=Feature.objects.all(),
                            widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    desired_condition = forms.CharField(required=False,
                            widget=forms.Textarea(attrs={'placeholder': '募集する選手の希望条件を入力してください', 'render_value': True}))
    disclosed = forms.BooleanField(required=False)


    def __init__(self, *args, **kwargs):
        super(TeamCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required':'{fieldname} は必須です。'.format(fieldname=field.label)}
            field.widget.attrs['class'] = 'form-control'
