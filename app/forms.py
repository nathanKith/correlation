from django import forms


class TickerForm(forms.Form):
    ticker1 = forms.CharField()
    ticker2 = forms.CharField()
