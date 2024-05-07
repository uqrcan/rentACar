from django.db import models
from django.core.validators import MaxLengthValidator
from django.conf import settings




class Customer(models.Model):

    class Meta:
        verbose_name_plural = 'Customers'
    pass


class Car(models.Model):
    plate_number = models.CharField(max_length=100, validators=[MaxLengthValidator(17)])  
    brand = models.CharField(max_length=50)  
    model = models.CharField(max_length=50)  
    year = models.PositiveSmallIntegerField()  
    gear = models.CharField(max_length=50)  
    rent_per_day = models.IntegerField()  
    availability = models.BooleanField(default=True)  

    def __str__(self):
        return f"{self.brand} {self.model} - {self.plate_number}"

class Reservation(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    car = models.ForeignKey(Car, on_delete=models.CASCADE)  
    start_date = models.DateField()  
    end_date = models.DateField() 

    def __str__(self):
        return f"Reservation for {self.car} by {self.customer} from {self.start_date} to {self.end_date}"

    class Meta:
        unique_together = ('customer', 'car', 'start_date', 'end_date')  # Eşsiz rezervasyon kombinasyonları için