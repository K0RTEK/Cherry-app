from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

from .models import AudioFile


# class CustomAuthenticationForm(AuthenticationForm):
#     def __init__(self, *args, **kwargs):
#         super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
#         self.fields['username'].widget.attrs['class'] = "form-control"
#         self.fields['password'].widget.attrs['class'] = "form-control"


class AudioUploadForm(forms.ModelForm):
    class Meta:
        model = AudioFile
        fields = ['audio']
