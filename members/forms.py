from django import forms
from .models import Member
class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)

class MemberForm(forms.ModelForm):
    class Meta:
        # specify model to be used
        model = Member

        # specify fields to be used
        fields = '__all__'
        widgets = {
            'joined_date': forms.DateInput(attrs={'type': 'date'})
        }