from django.shortcuts import render
from django_filters.views import FilterView

from .models import Product
from .filters import ProductFilter

# Create your views here.

class ProductList(FilterView):
    model = Product
    filterset_class = ProductFilter
    paginate_by = 2
