from django import forms
from .models import Notice
from .models import Forms


# forms.py  

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Forms
        fields = ['title', 'review_date', 'submission_date']



class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter notice title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter notice content', 'rows': 4}),
        }
