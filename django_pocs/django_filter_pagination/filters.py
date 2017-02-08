import django_filters

from .models import Product

class ProductFilter(django_filters.FilterSet):

    class Meta:
        model = Product
        fields = {
            'release_date': ['month__exact','year__exact'],
        }
