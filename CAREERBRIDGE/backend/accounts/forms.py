from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import re

User = get_user_model()

class StudentRegistrationForm(forms.Form):
    # User Account Fields
    full_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Enter your full name'}))
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Choose a username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'yourname@example.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Create a password'}))
    
    # Student Profile Fields
    college_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Your College/University'}))
    branch = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'e.g. Computer Science'}))
    year_of_study = forms.ChoiceField(choices=[
        (1, '1st Year'), (2, '2nd Year'), (3, '3rd Year'),
        (4, 'Final Year'), (5, 'Post Graduate'),
    ])
    
    # Verification Fields
    aadhaar_number = forms.CharField(
        max_length=12, 
        min_length=12, 
        widget=forms.TextInput(attrs={'placeholder': '12-digit Aadhaar Number'}),
        help_text="Your Aadhaar number will be securely hashed and never stored in plain text."
    )
    college_id_card = forms.ImageField(
        label="College ID Upload",
        help_text="Clear image of your official college ID card."
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    def clean_aadhaar_number(self):
        aadhaar = self.cleaned_data.get('aadhaar_number')
        # Basic validation: check if it's 12 digits
        if not re.match(r'^\d{12}$', aadhaar):
            raise ValidationError("Aadhaar number must be exactly 12 digits.")
        return aadhaar

    def clean_college_id_card(self):
        image = self.cleaned_data.get('college_id_card')
        if image:
            # Check file size (e.g., max 5MB)
            if image.size > 5 * 1024 * 1024:
                raise ValidationError("Image file size should not exceed 5MB.")
            
            # Check file extension/type (ImageField already does basic check, 
            # but we can be more specific if needed)
            valid_types = ['image/jpeg', 'image/png']
            if image.content_type not in valid_types:
                raise ValidationError("Only JPEG and PNG images are allowed.")
        return image
