from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Vehicles, Review, Profile


USER_TYPE_CHOICES = [
    (0, 'Customer'),
    (1, 'Owner'),
    (2, 'Admin'),
]


class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    user_type = forms.TypedChoiceField(
        label="Register As",
        choices=USER_TYPE_CHOICES,
        coerce=int,
        widget=forms.Select(
            attrs={
                "class": "form-control"
            }
        )
    )



    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    # using the values 1,2,3 to decide whether it's owner, customer or admin
    def save(self, commit=True):
        user = super().save(commit=False)   
        user_type = self.cleaned_data['user_type']
        if user_type == 2:
            user.is_admin = True
            user.is_owner = False
            user.is_customer = False
        elif user_type == 1:
            user.is_admin = False
            user.is_owner = True
            user.is_customer = False
        else:
            user.is_admin = False
            user.is_owner = False
            user.is_customer = True
        if commit:
            user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control custom-email-class'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name','profile_picture', 'phone_number']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control custom-full-name-class'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control custom-profile-picture-class'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control custom-phone-number-class'}),
            
        }


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicles
        fields = ['vehicle_model', 'rent_price', 'category', 'description', 'image']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)], attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }
