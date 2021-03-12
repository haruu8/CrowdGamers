from django import forms
from teams.models import Job, Notification



class InvitationCreateForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ('desired_job', 'message', 'invitation_url')

    desired_job = forms.ModelMultipleChoiceField(queryset=Job.objects.all(), required=True, label='希望枠',
                            help_text='1つまで選択することができます', widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    message = forms.CharField(required=True, label='メッセージ',
                                widget=forms.Textarea(attrs={'placeholder': '招待理由を入力してください', 'render_value': True}))
    invitation_url = forms.URLField(required=True, label='招待URL',
                                widget=forms.URLInput(attrs={'placeholder': '招待が承認された後に会話するDiscordのサーバー招待URLを入力してください', 'render_value': True}))

    def __init__(self, *args, **kwargs):
        super(InvitationCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required':'{fieldname} は必須です。'.format(fieldname=field.label)}
            field.widget.attrs['class'] = 'form-control'

    def clean_desired_job(self):
        """
        希望職の選択上限を1つに設定する validation

        TODO
        -----
        他で使用している関数とまとめる
        """
        desired_job = self.cleaned_data['desired_job']
        if len(desired_job) >= 2:
            raise forms.ValidationError('希望職は1つまでしか選択することができません')
        return desired_job
