from django import forms 
from .models import Blog
from django import forms
class LoginForm(forms.Form):
    # form fields here
        def save(self):
            user =  super().save(commit=False )
            password =  self.cleaned_data['password']
            user.set_password(password)
            return  user
class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title','content','category','image']
        labels={
            'title':'',
            'content':'',
            'category':'',
            'image':'',
        }
        widgets = {
            'image': forms.FileInput(attrs={'class': 'inputfile'}),
        }
