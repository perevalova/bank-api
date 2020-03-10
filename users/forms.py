from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserChangeForm(UserChangeForm):
    """
    Form for changing Custom User
    """
    class Meta:
        model = CustomUser
        fields = ('email',)


class UserSignupForm(UserCreationForm):
    """
    Form for Custom User authentication
    """
    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name')
