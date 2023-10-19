from django.contrib.auth.models import User
from django import forms
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from auth_apps.models import Profile


def ForbiddenUsers(value):
    forbidden_users = [
        'js', 'css', 'admin', 'python', 'java', 'join', 'user', 'username',
        'sql', 'root', 'login', 'logout', 'static', 'delete', 'auth', 'authenticate'
    ]

    if value.lower() in forbidden_users:
        raise ValidationError('This is a reserved word.')


def InvalidUsers(value):
    if '@' in value or '&' in value  or '$' in value or '-' in value or '+' in value or '*' in value or '#' in value:
        raise ValidationError('This is an invalid user, Do not user this caracter')


def UniqueEmail(value):
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError('User with this email  already exist')


def UniqueUser(value):
    if User.objects.filter(username__iexact=value).exists():
        raise ValidationError('User with this Username  already exist')

    

class SignupForm(forms.ModelForm):

    username = forms.CharField(max_length=200, widget=forms.TextInput(), required=True)
    email = forms.EmailField(max_length=200, widget=forms.EmailInput(), required=True)
    password = forms.CharField(max_length=40, min_length=6 , widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(max_length=40, min_length=6, widget=forms.PasswordInput())


    class Meta:
        model = User
        fields = ('username', 'email', 'password')
    

    def __init__(self, *args, **kwargs):

        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].validators.append(ForbiddenUsers)
        self.fields['username'].validators.append(InvalidUsers)
        self.fields['username'].validators.append(UniqueUser)
        self.fields['email'].validators.append(UniqueEmail)
    

    def clean(self):
        super(SignupForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            self._errors['password'] = self.error_class(['Password do not match. Please try again'])
        return self.cleaned_data

class ChangePasswordForm(forms.ModelForm):
	id = forms.CharField(widget=forms.HiddenInput())
	old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium'}), label="Old password", required=True)
	new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium'}), label="New password", required=True)
	confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium'}), label="Confirm new password", required=True)

	class Meta:
		model = User
		fields = ('id', 'old_password', 'new_password', 'confirm_password')

	def clean(self):
		super(ChangePasswordForm, self).clean()
		id = self.cleaned_data.get('id')
		old_password = self.cleaned_data.get('old_password')
		new_password = self.cleaned_data.get('new_password')
		confirm_password = self.cleaned_data.get('confirm_password')
		user = User.objects.get(pk=id)
		if not user.check_password(old_password):
			self._errors['old_password'] =self.error_class(['Old password do not match.'])
		if new_password != confirm_password:
			self._errors['new_password'] =self.error_class(['Passwords do not match.'])
		return self.cleaned_data



class EditeProfileForm(forms.ModelForm):
    picture = forms.ImageField(required=False)
    first_name = forms.CharField(max_length=200, widget=forms.TextInput(), required=False)
    last_name = forms.CharField(max_length=200, widget=forms.TextInput(), required=False)
    location = forms.CharField(max_length=200, widget=forms.TextInput(), required=False)
    url = forms.URLField(max_length=100, widget=forms.URLInput(), required=False)
    profile_info = forms.CharField( widget=forms.TextInput(), max_length=260, required=False)
    
    

    class Meta:
        model = Profile
        fields = ('picture', 'first_name', 'last_name', 'location', 'url', 'profile_info')
    
