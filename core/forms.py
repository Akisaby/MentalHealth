from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter Your Feedback'}),
        }

