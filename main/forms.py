from django import forms

class ImageForm(forms.Form):
    title =forms.CharField(max_length=100)
    desc =forms.CharField(max_length=200)
    img = forms.FileField()
    price = forms.IntegerField()
    condition =forms.CharField(max_length=10)
    location =forms.CharField(max_length=15)
