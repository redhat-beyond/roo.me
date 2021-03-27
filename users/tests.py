from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import transaction, IntegrityError


class UserTests(TestCase):

    def test_superuser(self):

        db = get_user_model()

        # Check if create_superuser creates a good superuser
        super_user = db.objects.create_superuser(
            'email@address.com', 'first_name', 'last_name', '1900-01-01', 'password'
        )
        self.assertEqual(super_user.email, 'email@address.com')
        self.assertEqual(super_user.first_name, 'first_name')
        self.assertEqual(super_user.last_name, 'last_name')
        self.assertEqual(super_user.birth_date, '1900-01-01')
        self.assertEqual(super_user.is_active, True)
        self.assertEqual(super_user.is_staff, True)
        self.assertEqual(super_user.is_superuser, True)
        self.assertEqual(str(super_user), 'email@address.com')

        # Check if email field is unique
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                db.objects.create_superuser(
                    'email@address.com', 'first_name', 'last_name', '1900-01-01', 'password'
                )

        # Check if create_superuser must have is_staff=True
        with self.assertRaises(ValueError):
            with transaction.atomic():
                db.objects.create_superuser(
                    'email_1@address.com', 'first_name', 'last_name', '1900-01-01', 'password', is_staff=False
                )

        # Check if create_superuser must have is_superuser=True
        with self.assertRaises(ValueError):
            with transaction.atomic():
                db.objects.create_superuser(
                    'email_2@address.com', 'first_name', 'last_name', '1900-01-01', 'password', is_superuser=False
                )

    def test_user(self):

        db = get_user_model()

        # Check if create_user creates a good user
        user = db.objects.create_user(
            'email@address.com', 'first_name', 'last_name', '1900-01-01', 'password'
        )
        self.assertEqual(user.email, 'email@address.com')
        self.assertEqual(user.first_name, 'first_name')
        self.assertEqual(user.last_name, 'last_name')
        self.assertEqual(user.birth_date, '1900-01-01')
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_superuser, False)
        self.assertEqual(str(user), 'email@address.com')

        # Check if email field is unique
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                db.objects.create_user(
                    'email@address.com', 'first_name', 'last_name', '1900-01-01', 'password'
                )

        # Check if create_user must have an email field
        with self.assertRaises(ValueError):
            with transaction.atomic():
                db.objects.create_user(
                    '', 'first_name', 'last_name', '1900-01-01', 'password'
                )

        # Check if create_user must have a first_name field
        with self.assertRaises(ValueError):
            with transaction.atomic():
                db.objects.create_user(
                    'email_1@address.com', '', 'last_name', '1900-01-01', 'password'
                )

        # Check if create_user must have a last_name field
        with self.assertRaises(ValueError):
            with transaction.atomic():
                db.objects.create_user(
                    'email_2@address.com', 'first_name', '', '1900-01-01', 'password'
                )

        # Check if create_user must have a birth_date field
        with self.assertRaises(ValueError):
            with transaction.atomic():
                db.objects.create_user(
                    'email_2@address.com', 'first_name', 'last_name', '', 'password'
                )
