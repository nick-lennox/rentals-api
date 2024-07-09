from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rentals.models import Rental, RentalType
from rentals.selectors import rental_list, reservation_list
from rentals.services import reservation_create


class ReservationApi(APIView):
    """
    API endpoint for managing reservations

    /rentals/reservation
    GET: Retrieve a list of reservations based on optional filters
    POST: Create a new reservation with given rental, start time, and end time

    InputSerializer: Serializer for validating and parsing incoming reservation data
    OutputSerializer: Serializer for formatting reservation data in API responses
    FilterSerializer: Serializer for validating and parsing optional query parameters for filtering reservations
    """

    class InputSerializer(serializers.Serializer):
        rental = serializers.PrimaryKeyRelatedField(
            queryset=Rental.objects.all(), required=True
        )
        start_time = serializers.DateTimeField(required=True)
        end_time = serializers.DateTimeField(required=True)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        rental = serializers.PrimaryKeyRelatedField(read_only=True)
        start_time = serializers.DateTimeField()
        end_time = serializers.DateTimeField()
        created_at = serializers.DateTimeField()

    class FilterSerializer(serializers.Serializer):
        rental = serializers.PrimaryKeyRelatedField(
            queryset=Rental.objects.all(), required=False
        )
        start_time = serializers.DateTimeField(required=False)
        end_time = serializers.DateTimeField(required=False)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        reservation_create(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)

    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        reservations = reservation_list(filters=filters_serializer.validated_data)

        data = self.OutputSerializer(reservations, many=True).data

        return Response(data)


class RentalApi(APIView):
    """
    API endpoint for managing rental properties

    /rentals/listings
    GET: Retrieve a list of rentals based on optional filters

    OutputSerializer: Serializer for formatting rental data in API responses
    FilterSerializer: Serializer for validating and parsing optional query parameters for filtering rentals
    """

    class OutputSerializer(serializers.Serializer):
        rental_type = serializers.PrimaryKeyRelatedField(read_only=True)
        name = serializers.CharField()

    class FilterSerializer(serializers.Serializer):
        rental_type = serializers.PrimaryKeyRelatedField(
            queryset=RentalType.objects.all(), required=False
        )
        name = serializers.CharField(max_length=100, allow_blank=True, required=False)

    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        rentals = rental_list(filters=filters_serializer.validated_data)

        data = self.OutputSerializer(rentals, many=True).data

        return Response(data)
