from django import forms
from common.utils.number_helpers import ir_phone_number
from common.utils.otp_helpers import verify_input_otp_of_receiver
from .models import Profile


class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["name", "avatar", "email", "phone_number", "city", "address"]


class ProfileVerifyOTPForReceiver(forms.Form):
    otp = forms.CharField(max_length=5, required=True)

    def __init__(self, *args, receiver=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.reciever = receiver

    def clean_otp(self):
        input = self.cleaned_data.get("otp")
        if not verify_input_otp_of_receiver(self.reciever, input):
            raise forms.ValidationError("Wrong otp code entered!")

        return input
