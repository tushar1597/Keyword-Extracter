from django import forms

class searchbox(forms.Form):
    searchvalue = forms.CharField(label='',max_length=30)

class NameForm(forms.Form):
    C = forms.CharField( widget=forms.Textarea ,help_text='Write here your message!')



