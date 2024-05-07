from rest_framework import status, views
from rest_framework.response import Response
from .serializers import UserSerializer, CarSerializer, ReservationSerializer
from .models import Customer, Car, Reservation
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class CustomerListView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        customers = Customer.objects.all()
        serializer = UserSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerDetailView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        customer = self.get_object(pk)
        serializer = UserSerializer(customer)
        return Response(serializer.data)

    def put(self, request, pk):
        customer = self.get_object(pk)
        serializer = UserSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        customer = self.get_object(pk)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CarListView(views.APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CarDetailView(views.APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self, pk):
        try:
            return Car.objects.get(pk=pk)
        except Car.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        car = self.get_object(pk)
        serializer = CarSerializer(car)
        return Response(serializer.data)

    def put(self, request, pk):
        car = self.get_object(pk)
        serializer = CarSerializer(car, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        car = self.get_object(pk)
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ReservationListView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reservations = Reservation.objects.filter(customer=request.user)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            # Kullanıcının aynı tarihte başka bir rezervasyonu olup olmadığını kontrol
            same_date_reservation = Reservation.objects.filter(
                customer=request.user, 
                start_date__lte=serializer.validated_data['end_date'], 
                end_date__gte=serializer.validated_data['start_date']
            ).exists()
            if same_date_reservation:
                return Response({'error': 'Zaten bu tarihler arasında bir rezervasyonunuz var.'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save(customer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReservationDetailView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Reservation.objects.get(pk=pk, customer=self.request.user)
        except Reservation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        reservation = self.get_object(pk)
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)

    def put(self, request, pk):
        reservation = self.get_object(pk)
        serializer = ReservationSerializer(reservation, data=request.data, partial=True)
        if serializer.is_valid():
            if 'end_date' in serializer.validated_data:
                # Bitiş tarihinin uzatılmasının mümkün olup olmadığını kontrol
                overlap = Reservation.objects.filter(
                    car=reservation.car,
                    start_date__lte=serializer.validated_data['end_date'],
                    end_date__gte=reservation.start_date
                ).exclude(pk=reservation.pk).exists()
                if overlap:
                    return Response({'error': 'Bu tarihler arasında araç zaten başka bir müşteri tarafından rezerve edilmiş.'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        reservation = self.get_object(pk)
        reservation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class ReservationListView(views.APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         reservations = Reservation.objects.filter(customer=request.user)
#         serializer = ReservationSerializer(reservations, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = ReservationSerializer(data=request.data)
#         if serializer.is_valid():
#             # Kullanıcının aynı tarihte başka bir rezervasyonu olup olmadığını kontrol
#             same_date_reservation = Reservation.objects.filter(
#                 customer=request.user, 
#                 start_date__lte=serializer.validated_data['end_date'], 
#                 end_date__gte=serializer.validated_data['start_date']
#             ).exists()
#             if same_date_reservation:
#                 return Response({'error': 'Zaten bu tarihler arasında bir rezervasyonunuz var.'}, status=status.HTTP_400_BAD_REQUEST)

#             serializer.save(customer=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ReservationDetailView(views.APIView):
#     permission_classes = [IsAuthenticated]

#     def get_object(self, pk):
#         try:
#             return Reservation.objects.get(pk=pk, customer=self.request.user)
#         except Reservation.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#     def get(self, request, pk):
#         reservation = self.get_object(pk)
#         serializer = ReservationSerializer(reservation)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         reservation = self.get_object(pk)
#         serializer = ReservationSerializer(reservation, data=request.data, partial=True)
#         if serializer.is_valid():
#             if 'end_date' in serializer.validated_data:
#                 # Bitiş tarihinin uzatılmasının mümkün olup olmadığını kontrol
#                 overlap = Reservation.objects.filter(
#                     car=reservation.car,
#                     start_date__lte=serializer.validated_data['end_date'],
#                     end_date__gte=reservation.start_date
#                 ).exclude(pk=reservation.pk).exists()
#                 if overlap:
#                     return Response({'error': 'Bu tarihler arasında araç zaten başka bir müşteri tarafından rezerve edilmiş.'}, status=status.HTTP_400_BAD_REQUEST)
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         reservation = self.get_object(pk)
#         reservation.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
