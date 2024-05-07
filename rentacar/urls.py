from django.urls import path
from .views import CustomerListView, CustomerDetailView, CarListView, CarDetailView, ReservationListView, ReservationDetailView

urlpatterns = [
    
    # Customer URLs
    path('customers/', CustomerListView.as_view(), name='customer-list'),
    path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),
    
    # Car URLs
    path('cars/', CarListView.as_view(), name='car-list'),
    path('cars/<int:pk>/', CarDetailView.as_view(), name='car-detail'),
    
    # Reservation URLs
    path('reservations/', ReservationListView.as_view(), name='reservation-list'),
    path('reservations/<int:pk>/', ReservationDetailView.as_view(), name='reservation-detail'),
]
