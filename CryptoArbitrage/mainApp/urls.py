from django.urls import path
from .views import OnePairArbitrageView


urlpatterns = [
    path('', OnePairArbitrageView.as_view(), name='Main view'),

]
