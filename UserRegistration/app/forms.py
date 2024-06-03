from django import forms


from app.models import *

class Userform(forms.ModelForm):
    class Meta():
        model=User
        fields=['username','email','password']
        widgets={'password':forms.PasswordInput}
        help_texts={'username':''}

class Profileform(forms.ModelForm):
    class Meta():
        model=Profile
        fields=['address','profile_pic']
        widgets={'address':forms.Textarea(attrs={'cols':25,'rows':3})}
