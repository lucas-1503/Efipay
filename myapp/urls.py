from django.urls import path
from . import views
from .views import CreateChargeView, ChargeDetailView



urlpatterns = [
    path('charge/create/', CreateChargeView.as_view(), name='create_charge'),
    path('charge/<int:charge_id>/', ChargeDetailView.as_view(), name='charge_detail'),
    path('autenticate/', views.authenticate_view, name='autenticate')
]
