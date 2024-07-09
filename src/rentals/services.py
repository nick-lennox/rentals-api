from datetime import date

from rentals.models import Reservation


def reservation_create(*, rental: int, start_time: date, end_time: date) -> Reservation:
    obj = Reservation(rental=rental, start_time=start_time, end_time=end_time)

    obj.full_clean()
    obj.save()

    return obj
