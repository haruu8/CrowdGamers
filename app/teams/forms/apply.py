from django import forms
from teams.models import Apply, Job



class ApplyCreateForm(forms.ModelForm):
    class Meta:
        model = Apply
        fields = ('desired_job', 'message')
        labels = {
            'desired_job': '希望職',
            'message': '志望理由',
        }

    desired_job = forms.ModelMultipleChoiceField(queryset=Job.objects.all(), required=True, help_text='1つまで選択することができます',
                            widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    message = forms.CharField(required=True,
                                widget=forms.Textarea(attrs={'placeholder': '志望理由を入力してください', 'render_value': True}))

    def __init__(self, *args, **kwargs):
        super(ApplyCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required':'{fieldname} は必須です。'.format(fieldname=field.label)}
            field.widget.attrs['class'] = 'form-control'

    # 希望職を1つまでしか選択できないようにする validation
    def clean_desired_job(self):
        desired_job = self.cleaned_data['desired_job']
        if len(desired_job) >= 2:
            raise forms.ValidationError('希望職は1つまでしか選択することができません')
        return desired_job
