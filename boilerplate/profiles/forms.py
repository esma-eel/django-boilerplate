from django import forms
from .models import ProfilePhoneNumber, Profile, ProfileEmail


class ProfilePhoneNumberModelForm(forms.ModelForm):
    class Meta:
        model = ProfilePhoneNumber
        fields = ["phone_number", "is_primary"]


class ProfileEmailModelForm(forms.ModelForm):
    class Meta:
        model = ProfileEmail
        fields = ["email", "is_primary"]


class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["name", "avatar"]


ProfilePhoneNumberModelFormSet = forms.modelformset_factory(
    model=ProfilePhoneNumber,
    form=ProfilePhoneNumberModelForm,
    fields=ProfilePhoneNumberModelForm.Meta.fields,
)

ProfileEmailModelFormSet = forms.modelformset_factory(
    model=ProfileEmail,
    form=ProfileEmailModelForm,
    fields=ProfileEmailModelForm.Meta.fields,
)
