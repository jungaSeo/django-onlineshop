from django import forms

class AddProductForm(forms.Form):
    quantity = forms.IntegerField()
    is_update = forms.BooleanField(required=False,
                                   initial=False,
                                   widget=forms.HiddenInput)
    # form 안에 안보이는 값들 처리시
