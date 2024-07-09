from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from rentals.models import Rental, RentalType, Reservation


class RentalModelTest(TestCase):
    def setUp(self):
        self.rental_type = RentalType.objects.create(name="Beach house", limit=2)
        Rental.objects.create(rental_type=self.rental_type)
        Rental.objects.create(rental_type=self.rental_type)

    def test_rental_limit_exceeded(self):
        with self.assertRaises(ValidationError):
            rental3 = Rental(rental_type=self.rental_type, name="Rental 3")
            rental3.full_clean()
            rental3.save()

    def test_rental_limit_not_exceeded(self):
        rental_type = RentalType.objects.create(name="Lake house", limit=1)
        rental = Rental(rental_type=rental_type, name="Loot Lake Lodge")
        rental.full_clean()
        rental.save()
        self.assertEqual(Rental.objects.filter(rental_type=rental_type).count(), 1)


class ReservationModelTest(TestCase):
    def setUp(self):
        self.rental_type = RentalType.objects.create(name="Beach house")
        self.rental = Rental.objects.create(
            rental_type=self.rental_type, name="Beachfront Bargain"
        )
        self.reservation = Reservation.objects.create(
            rental=self.rental,
            start_time=timezone.now() + timedelta(days=5),
            end_time=timezone.now() + timedelta(days=10),
        )

    # |-<date range A>-| |-<date range B>-|
    def test_non_overlapping(self):
        new_start_time = self.reservation.end_time + timedelta(days=1)
        new_end_time = new_start_time + timedelta(days=5)
        reservation = Reservation(
            rental=self.reservation.rental,
            start_time=new_start_time,
            end_time=new_end_time,
        )
        reservation.full_clean()
        reservation.save()
        self.assertEqual(Reservation.objects.count(), 2)

    #       |-<date range A>-|
    #   |-<date range B>-|
    def test_partial_overlap_before(self):
        overlap_start_time = self.reservation.start_time - timedelta(days=1)
        overlap_end_time = self.reservation.start_time + timedelta(days=1)
        reservation = Reservation(
            rental=self.reservation.rental,
            start_time=overlap_start_time,
            end_time=overlap_end_time,
        )
        with self.assertRaises(ValidationError):
            reservation.full_clean()
            reservation.save()

    #   |-<date range A>-|
    #       |-<date range B>-|
    def test_partial_overlap_after(self):
        overlap_start_time = self.reservation.end_time - timedelta(days=1)
        overlap_end_time = self.reservation.end_time + timedelta(days=1)
        reservation = Reservation(
            rental=self.reservation.rental,
            start_time=overlap_start_time,
            end_time=overlap_end_time,
        )
        with self.assertRaises(ValidationError):
            reservation.full_clean()
            reservation.save()

    # |---<date range A>---|
    #   |-<date range B>-|
    def test_partial_overlap_within(self):
        overlap_start_time = self.reservation.start_time + timedelta(days=1)
        overlap_end_time = self.reservation.end_time - timedelta(days=1)
        reservation = Reservation(
            rental=self.reservation.rental,
            start_time=overlap_start_time,
            end_time=overlap_end_time,
        )
        with self.assertRaises(ValidationError):
            reservation.full_clean()
            reservation.save()
