from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from rentals.models import Rental, RentalType, Reservation


class ReservationApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.rental_type = RentalType.objects.create(name="Beach house")
        self.rental = Rental.objects.create(rental_type=self.rental_type)

        now = timezone.now()
        Reservation.objects.create(
            rental=self.rental,
            start_time=now + timedelta(days=5),
            end_time=now + timedelta(days=6),
        )
        Reservation.objects.create(
            rental=self.rental,
            start_time=now + timedelta(days=10),
            end_time=now + timedelta(days=15),
        )
        Reservation.objects.create(
            rental=self.rental,
            start_time=now + timedelta(days=20),
            end_time=now + timedelta(days=25),
        )

    def test_create_reservation(self):
        start_time = timezone.now() + timedelta(days=1)
        end_time = start_time + timedelta(days=2)

        data = {
            "rental": self.rental.id,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
        }

        response = self.client.post("/rentals/reservation", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 4)

    def test_list_reservations(self):
        response = self.client.get("/rentals/reservation")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_filter_reservations_by_rental(self):
        response = self.client.get("/rentals/reservation", {"rental": self.rental.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_filter_reservations_by_start_time(self):
        filter_start_time = timezone.now() + timedelta(days=12)
        response = self.client.get(
            "/rentals/reservation", {"start_time": filter_start_time.isoformat()}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_reservations_by_end_time(self):
        filter_end_time = timezone.now() + timedelta(days=18)
        response = self.client.get(
            "/rentals/reservation", {"end_time": filter_end_time.isoformat()}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_reservations_by_start_and_end_time(self):
        filter_start_time = timezone.now() + timedelta(days=12)
        filter_end_time = timezone.now() + timedelta(days=22)
        response = self.client.get(
            "/rentals/reservation",
            {
                "start_time": filter_start_time.isoformat(),
                "end_time": filter_end_time.isoformat(),
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_reservations_with_no_result(self):
        filter_start_time = timezone.now() + timedelta(days=30)
        filter_end_time = timezone.now() + timedelta(days=40)
        response = self.client.get(
            "/rentals/reservation",
            {
                "start_time": filter_start_time.isoformat(),
                "end_time": filter_end_time.isoformat(),
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


class RentalApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.rental_type1 = RentalType.objects.create(name="Beach house")
        self.rental_type2 = RentalType.objects.create(name="Lake house")
        Rental.objects.create(rental_type=self.rental_type1, name="Beachfront Bargain")
        Rental.objects.create(rental_type=self.rental_type2, name="Loot Lake Lodge")

    def test_list_rentals(self):
        response = self.client.get("/rentals/listings")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_rentals_by_type(self):
        response = self.client.get(
            "/rentals/listings", {"rental_type": self.rental_type1.id}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Beachfront Bargain")
