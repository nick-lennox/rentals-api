from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from core.settings import DEFAULT_RENTAL_LIMIT


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class RentalType(BaseModel):
    name = models.CharField(max_length=50, null=False, blank=False)
    limit = models.PositiveIntegerField(
        default=DEFAULT_RENTAL_LIMIT, null=False, blank=False
    )

    def __str__(self):
        return self.name


class Rental(BaseModel):
    rental_type = models.ForeignKey(RentalType, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100, null=False, blank=False)

    def clean(self):
        # Ensure limit is not exceeded when adding a new rental
        if self.rental_type and self._state.adding:
            curr_rental_type_count = Rental.objects.filter(
                rental_type=self.rental_type
            ).count()
            if curr_rental_type_count >= self.rental_type.limit:
                raise ValidationError(
                    f"The limit of {self.rental_type.limit} rentals for {self.rental_type.name} has been reached"
                )

    def __str__(self):
        return self.name


class Reservation(BaseModel):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)

    start_time = models.DateTimeField(null=False, blank=False)
    end_time = models.DateTimeField(null=False, blank=False)

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("Start time must precede end time")

        overlapping_reservations = Reservation.objects.filter(
            rental=self.rental,
            start_time__lte=self.end_time,
            end_time__gte=self.start_time,
        ).exists()

        if overlapping_reservations:
            raise ValidationError("Rental unavailable")

    def __str__(self):
        return f"Reservation for {self.rental.name} from {self.start_time} to {self.end_time}"
