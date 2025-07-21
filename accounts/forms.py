from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'phone_number', 'city', 'country']
        exclude = ['role', 'user', 'is_approved']  # Exclude role, user, and is_approved from the form

        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number',
                'pattern': r'\+?\d{0,15}',
                'title': 'Phone number can include the country code and should contain only digits.',
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your city',
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your country',
            }),
            'role': forms.Select(attrs={
                'class': 'form-control',
                'disabled': 'disabled',  # Prevents users from changing their role
            }),
        }
        
        labels = {
            'profile_picture': 'Profile Picture',
            'phone_number': 'Phone Number',
            'city': 'City',
            'country': 'Country',
            'role': 'Role',
        }

        help_texts = {
            'profile_picture': 'Upload a profile picture (optional).',
            'phone_number': 'Include your country code if applicable.',
            'city': 'Your current city of residence.',
            'country': 'Your country of residence.',
            'role': 'Your role on the platform. Only an admin can change this.',
        }
        
        
    def save(self, commit=True):
        profile = super().save(commit=False)
        # Ensure the role field remains unchanged
        original_role = Profile.objects.get(pk=profile.pk).role
        profile.role = original_role
        if commit:
            profile.save()
        return profile
