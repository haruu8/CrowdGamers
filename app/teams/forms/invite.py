from django import forms
from teams.models import Job, Notification



class InviteCreateForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ('desired_job', 'message', 'invite_url')
        labels = {
            'desired_job': '希望職',
            'message': 'メッセージ',
            'invite_url': '招待用URL',
        }

    desired_job = forms.ModelMultipleChoiceField(queryset=Job.objects.all(), required=True, help_text='1つまで選択することができます',
                            widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    message = forms.CharField(required=True,
                                widget=forms.Textarea(attrs={'placeholder': '招待理由を入力してください', 'render_value': True}))
    invite_url = forms.URLField(required=True,
                                widget=forms.URLInput(attrs={'placeholder': '招待が承認された後に会話するDiscordのサーバー招待URLを入力してください', 'render_value': True}))

    def __init__(self, *args, **kwargs):
        super(InviteCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required':'{fieldname} は必須です。'.format(fieldname=field.label)}
            field.widget.attrs['class'] = 'form-control'

    # 希望職を1つまでしか選択できないようにする validation
    def clean_desired_job(self):
        desired_job = self.cleaned_data['desired_job']
        if len(desired_job) >= 2:
            raise forms.ValidationError('希望職は1つまでしか選択することができません')
        return desired_job
