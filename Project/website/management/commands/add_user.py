
from django.core.management.base import BaseCommand
from website.models import CustomUser 

class Command(BaseCommand):
    help = 'Adds a new user to the system'

    def handle(self, *args, **kwargs):
        # Your logic for adding users goes here
        username = input("Enter username: ")
        password = input("Enter password: ")
        email = input("Enter email: ")

        # Create the user using CustomUser model
        user = CustomUser.objects.create_user(username=username, email=email, password=password)

        self.stdout.write(self.style.SUCCESS(f"User '{username}' created successfully"))