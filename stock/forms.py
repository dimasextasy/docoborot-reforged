from django import forms
from django.contrib.admin.widgets import AdminDateWidget

from .models import Partner, Stock, Product, Deal, DealProduct


class SignatureFileForm(forms.Form):
    report = forms.FileField()
    signature = forms.FileField()
    public_key = forms.FileField()


class ReportModelForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = ['partner_id']


class ReportDateForm(forms.Form):
    start_date = forms.DateField(widget=forms.SelectDateWidget(years=range(2015, 2025)))
    finish_date = forms.DateField(widget=forms.SelectDateWidget(years=range(2015, 2025)))


class DealModelForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = ['deal_type', 'partner_id', 'date']


class DealProductModelForm(forms.ModelForm):
    class Meta:
        model = DealProduct
        fields = ['product_id', 'count']


class PartnerModelForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ['name', 'surname', 'patronymic', 'company_name']

    def clean_company_name(self, *args, **kwargs):
        instance = self.instance
        company_name = self.cleaned_data.get('company_name')
        qs = Partner.objects.filter(company_name__iexact=company_name)
        if instance is not None:
            qs = qs.exclude(pk=instance.pk) # id=instance.id
        if qs.exists():
            raise forms.ValidationError("Такое наименование уже используется, попробуйте ввести другое.")
        return company_name

class StockModelForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['name']

    def clean_name(self, *args, **kwargs):
        instance = self.instance
        name = self.cleaned_data.get('name')
        qs = Stock.objects.filter(name__iexact=name)
        if instance is not None:
            qs = qs.exclude(pk=instance.pk) # id=instance.id
        if qs.exists():
            raise forms.ValidationError("Такое наименование уже используется, попробуйте ввести другое.")
        return name

class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'purchase_price', 'selling_price', 'stock_id']

    def clean_name(self, *args, **kwargs):
        instance = self.instance
        name = self.cleaned_data.get('name')
        qs = Product.objects.filter(name__iexact=name)
        if instance is not None:
            qs = qs.exclude(pk=instance.pk) # id=instance.id
        if qs.exists():
            raise forms.ValidationError("Такое наименование уже используется, попробуйте ввести другое.")
        return name
