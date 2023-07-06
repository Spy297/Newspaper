from django import forms
from .models import Comment  # Assuming you have a Comment model defined

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
