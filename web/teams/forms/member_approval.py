from django import forms
from teams.models import Notification



class MemberApprovalCreateForm(forms.ModelForm):
    """
    メンバー追加申請のフォーム。
    """
    class Meta:
        model = Notification
        fields = ('message',)

    message = forms.CharField(required=True, label='メッセージ',
                            widget=forms.Textarea(attrs={'placeholder': 'オーナーにわかるようにメッセージを入力してください', 'render_value': True}))

    def __init__(self, *args, **kwargs):
        """
        一括でエラーメッセージを設定する。
        """
        super(MemberApprovalCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required':'{fieldname} は必須です。'.format(fieldname=field.label)}
            field.widget.attrs['class'] = 'form-control'
