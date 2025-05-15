from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body', 'email', 'rating',]
        widgets = {
            'rating': forms.NumberInput(attrs={'required': False}),
        }