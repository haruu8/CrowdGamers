from django import forms
from teams.models import Apply



class TeamApplyCreateForm(forms.ModelForm):
    class Meta:
        model = Apply
        fields = ('message',)
        labels = {
            'message': '志望理由',
        }

    message = forms.CharField(required=True,
                                widget=forms.Textarea(attrs={'placeholder': '志望理由を入力してください', 'render_value': True}))

    def __init__(self, *args, **kwargs):
        super(TeamApplyCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required':'{fieldname} は必須です。'.format(fieldname=field.label)}
            field.widget.attrs['class'] = 'form-control'
