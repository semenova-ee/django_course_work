from django import forms

from mailing.models import Client, Message, Mailing

class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class ClientForm(StyleFormMixin, forms.ModelForm):

    class Meta():
        model = Client
        exclude = ('owner',)
        fields = ['email', 'name','comment', 'is_active']


class MessageForm(StyleFormMixin, forms.ModelForm):

    class Meta():
        model = Message
        exclude = ('owner',)
        fields = ['title', 'text']

    def clean_title(self):
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        title = self.cleaned_data.get('title', '')
        for word in forbidden_words:
            if word in title.lower():
                raise forms.ValidationError(f"The word '{word}' is not allowed in the product name.")
        return title

    def clean_text(self):
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        text = self.cleaned_data.get('text', '')
        for word in forbidden_words:
            if word in text.lower():
                raise forms.ValidationError(f"The word '{word}' is not allowed in the message description.")
        return text

class MailingForm(StyleFormMixin, forms.ModelForm):

    class Meta():
        model = Mailing
        exclude = ['created_at', 'is_active', 'status', 'owner']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'clients':
                field.widget.attrs['class'] = 'form-control'