from django import forms

class LoginForm(forms.Form):
    agent_id = forms.CharField(label='Agent ID',widget=forms.TextInput(attrs={'class':'form-control'}))
    username = forms.CharField(label='Username',widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
class LoginFormStaff(forms.Form):
    username = forms.CharField(label='Username',widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    


    


