from django.conf.urls import url

from .views import ProductList

urlpatterns = [
    url(r'^product/$', ProductList.as_view(), name='django_filter_pagination_product_list'),
]
