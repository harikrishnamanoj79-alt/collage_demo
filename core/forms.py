"""
Forms for the college website.
"""

from django import forms
from .models import ContactMessage, AdmissionInquiry


class ContactForm(forms.ModelForm):
    """
    Contact form — submitted data is saved as a ContactMessage in the database.
    The admin can view all messages in the admin panel.
    """
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your Full Name',
                'class': 'form-input',
                'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Your Email Address',
                'class': 'form-input',
                'autocomplete': 'email',
            }),
            'subject': forms.TextInput(attrs={
                'placeholder': 'Subject',
                'class': 'form-input',
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Write your message here...',
                'class': 'form-textarea',
                'rows': 5,
            }),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise forms.ValidationError("Please enter your full name.")
        return name

    def clean_message(self):
        message = self.cleaned_data.get('message', '').strip()
        if len(message) < 10:
            raise forms.ValidationError("Please write a more detailed message (at least 10 characters).")
        return message


class AdmissionInquiryForm(forms.ModelForm):
    """
    Admission enquiry form shown on the homepage.
    """
    class Meta:
        model = AdmissionInquiry
        fields = ['name', 'email', 'phone', 'city', 'program_interest', 'current_qualification', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Student Name',
                'class': 'form-input',
                'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email Address',
                'class': 'form-input',
                'autocomplete': 'email',
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Phone Number',
                'class': 'form-input',
                'autocomplete': 'tel',
            }),
            'city': forms.TextInput(attrs={
                'placeholder': 'City',
                'class': 'form-input',
            }),
            'program_interest': forms.Select(
                choices=[
                    ('', 'Select Program'),
                    ('B.Tech', 'B.Tech'),
                    ('M.Tech', 'M.Tech'),
                    ('Diploma / Lateral Entry', 'Diploma / Lateral Entry'),
                    ('Certificate Program', 'Certificate Program'),
                ],
                attrs={'class': 'form-input'}
            ),
            'current_qualification': forms.TextInput(attrs={
                'placeholder': 'Current Qualification',
                'class': 'form-input',
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Tell us what program or support you are looking for...',
                'class': 'form-textarea',
                'rows': 4,
            }),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise forms.ValidationError("Please enter a valid student name.")
        return name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        digits = ''.join(ch for ch in phone if ch.isdigit())
        if len(digits) < 10:
            raise forms.ValidationError("Please enter a valid phone number.")
        return phone
