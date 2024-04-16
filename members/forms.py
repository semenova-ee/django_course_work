from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from members.models import User


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'is_active':
                field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        """
        Проверка email на уникальность
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Такой email уже используется в системе')
        return email


class UserForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'country', 'phone', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        phone_number = self.fields['phone'].widget

        self.fields['password'].widget = forms.HiddenInput()
        phone_number.attrs['class'] = "form-control bfh-phone"
        phone_number.attrs['data-format'] = "+7 (ddd) ddd-dd-dd"


class PasswordRecoveryForm(forms.Form):
    email = forms.EmailField(label='Email')

    def clean_email(self):
        """
        Проверка email на уникальность
        """
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('Такого email нет в системе')
        return email