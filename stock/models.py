from django.db import models


class Stock(models.Model):
    name = models.CharField(max_length=120)
    def __str__(self): return self.name


class Product(models.Model):
    name = models.CharField(max_length=120)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_id = models.ForeignKey(Stock, default=1, on_delete=models.CASCADE, null=False)
    def __str__(self): return self.name
    def get_id(self): return self.id


class Partner(models.Model):
    name = models.CharField(max_length=120)
    surname = models.CharField(max_length=120)
    patronymic = models.CharField(max_length=120)
    company_name = models.CharField(max_length=120)
    def __str__(self): return self.company_name


class DealType(models.Model):
    value = models.CharField(max_length=120)
    def __str__(self): return self.value


class Deal(models.Model):
    partner_id = models.ForeignKey(Partner, default=1, on_delete=models.CASCADE, null=False)
    date = models.DateField()
    deal_type = models.ForeignKey(DealType, default=1, on_delete=models.CASCADE, null=False)


class DealProduct(models.Model):
    deal_id = models.ForeignKey(Deal, default=1, on_delete=models.CASCADE, null=False)
    product_id = models.ForeignKey(Product, default=1, on_delete=models.CASCADE, null=False)
    count = models.IntegerField()