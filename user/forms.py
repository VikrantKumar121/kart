from django import forms
from .models import User, UserProfile

class RegistrationForm(forms.ModelForm):
    """"""

    password = forms.CharField(widget = forms.PasswordInput(attrs={
        'placeholder':'Enter password',
    }))

    confirm_password = forms.CharField(widget = forms.PasswordInput(attrs={
        'placeholder':'Confirm password',
    }))

    class Meta:
        model = User
        fields = [
            'user_name',
            'first_name',
            'last_name',
            'email',
            'phone_no',
            'password'
        ]

    # def clean(self):
    #     cleaned_data = super(RegistrationForm, self).clean()
    #     password = cleaned_data.get('password')
    #     confirm_password = cleaned_data.get('confirm_password')
    #
    #     if password != confirm_password :
    #         raise forms.ValidationError(
    #             'Password does not match'
    #         )


    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class UserForm(forms.ModelForm):
    """"""
    class Meta:
        model = User
        fields = (
        'first_name',
        'last_name',
        'phone_no',
        )

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class UserProfileForm(forms.ModelForm):
    """"""
    class Meta:
        model = UserProfile
        fields = (
            'address_line_1',
            'address_line_2',
            'city',
            'state',
            'country',
            'profile_pic',
        )

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
