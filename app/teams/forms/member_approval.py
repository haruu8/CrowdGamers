from django import forms
from teams.models import MemberApproval



class MemberApprovalCreateForm(forms.ModelForm):
    """
    メンバー追加申請のフォーム
    """
    class Meta:
        model = MemberApproval
        fields = ('message',)
        labels = {
            'message': 'メッセージ',
        }

    message = forms.CharField(required=True,
                            widget=forms.Textarea(attrs={'placeholder': 'オーナーにわかるようにメッセージを入力してください', 'render_value': True}))
