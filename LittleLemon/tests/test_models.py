from datetime import datetime
from django.test import TestCase
from restaurant.models import Menu, Booking

class MenuTest(TestCase):
    def test_get_item(self):
        item = Menu.objects.create(title="IceCream", price=80)
        self.assertEqual(item.__str__(), "IceCream : 80")
    

class BookingTest(TestCase):

    def test_create_booking(self):
        booking = Booking.objects.create(
            name="John Doe",
            no_of_guests=4,
            reservation_date=datetime(2024, 12, 1, 18, 0)
        )
        expected_str = "John Doe for 4 guests on 2024-12-01 18:00:00"
        self.assertEqual(str(booking), expected_str)

    def test_default_number_of_guests(self):
        booking = Booking.objects.create(
            name="Jane Doe",
            reservation_date=datetime(2024, 12, 1, 19, 0)
        )
        self.assertEqual(booking.no_of_guests, 1)