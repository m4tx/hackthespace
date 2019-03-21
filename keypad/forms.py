from django import forms


class KeypadForm(forms.Form):
    code = forms.CharField(max_length=7)

    def clean_code(self):
        code = self.cleaned_data['code']
        if code != '4254292':
            raise forms.ValidationError("Invalid code")
        return code
