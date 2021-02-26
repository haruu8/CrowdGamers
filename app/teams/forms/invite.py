from django import forms
from teams.models import Invite



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
