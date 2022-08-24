from django.db import models
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User


class AmazonPage(models.Model):
    url = models.TextField()
    product_name = models.CharField(max_length=255)

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        """Returns the URL to access a particular product instance."""
        return reverse('product-detail', args=[str(self.id)])


class ProductInstance(models.Model):
    product = models.ForeignKey('AmazonPage', on_delete=models.RESTRICT, null=True)
    product_price = models.FloatField()
    day_of_check = models.DateField()

    def __str__(self):
        return f'{self.product.__str__()}, {str(self.product_price)}'


class FollowedAmazonPages(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey('AmazonPage', on_delete=models.RESTRICT, null=True)

    def __str__(self):
        return f'{self.user}, {str(self.product.__str__())}'
