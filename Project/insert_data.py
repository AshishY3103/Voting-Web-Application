import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
django.setup()

from website.models import CustomUser, Poll, Choice

def insert_sample_data():
    # Create sample users
    user1 = CustomUser.objects.create_user(username='user1', email='user1@example.com', password='password1')
    user2 = CustomUser.objects.create_user(username='user2', email='user2@example.com', password='password2')

    # Create sample polls
    poll1 = Poll.objects.create(question='Sample poll 1', created_by=user1)
    poll2 = Poll.objects.create(question='Sample poll 2', created_by=user2)

    # Create choices for each poll
    Choice.objects.create(poll=poll1, choice_text='Choice A')
    Choice.objects.create(poll=poll1, choice_text='Choice B')
    Choice.objects.create(poll=poll2, choice_text='Choice C')
    Choice.objects.create(poll=poll2, choice_text='Choice D')

if __name__ == '__main__':
    insert_sample_data()
