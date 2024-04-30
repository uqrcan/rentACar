from rest_framework import serializers
from .models import Car, Reservation
from django.contrib.auth import get_user_model

User = get_user_model()

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'plate_number', 'brand', 'model', 'year', 'gear', 'rent_per_day', 'availability']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ReservationSerializer(serializers.ModelSerializer):
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all())
    customer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Reservation
        fields = ['id', 'customer', 'car', 'start_date', 'end_date']

    def validate(self, attrs):
        car = attrs['car']
        start_date = attrs['start_date']
        end_date = attrs['end_date']

        if Reservation.objects.filter(car=car, start_date_lte=end_date, end_date_gte=start_date).exists():
            raise serializers.ValidationError("This car is already reserved for the selected dates.")
        return attrs