from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse
from .models import Poll,Choice,CustomUser,Vote
from django.contrib.auth import authenticate, login,logout
from django.utils import timezone

from django.contrib.auth.hashers import make_password

from django.urls import reverse

def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('polls_list'))  # Redirect to the polls list page after successful login
        else:
            # Authentication failed
            error_message = "Invalid username or password. Please try again."
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def custom_register_view(request):
    if request.method == 'POST':
        # Extract user input from the request
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        name = request.POST.get('name')

        # Validate passwords match
        if password != confirm_password:
            error_message = "Passwords do not match. Please try again."
            return render(request, 'register.html', {'error_message': error_message})

        # Check if the username already exists
        if CustomUser.objects.filter(username=username).exists():
            error_message = "Username is already taken. Please choose a different one."
            return render(request, 'register.html', {'error_message': error_message})

        # Create the CustomUser instance
        user = CustomUser(username=username, password=make_password(password), name=name, register_on=timezone.now(), status="Active")
        user.save()

        # Redirect to login page after successful registration
        return redirect('login')
    else:
        return render(request, 'register.html')
 

@login_required
def create_poll(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        choices = request.POST.get('choices').split(',')  # Split choices by comma

        # Get the current user
        current_user = request.user

        # Create the poll
        poll = Poll.objects.create(question=question, created_by=current_user, pub_date=timezone.now())

        # Create choices for the poll
        for choice_text in choices:
            Choice.objects.create(poll=poll, choice_text=choice_text.strip())  # Remove leading/trailing whitespace

        # Redirect to a success page or to the poll list
        return redirect('polls_list')
    
    return render(request, 'create_poll.html')

@login_required
def polls_list(request):
    
    polls = Poll.objects.annotate(total_votes=Sum('choice__votes'))       
    return render(request,'polls_list.html',{'polls': polls})
    
@login_required
def vote_poll(request, poll_id):
    # Retrieve the poll object with the given poll ID from the database
    poll = get_object_or_404(Poll, pk=poll_id)
    
    # Check if the user has already voted for this poll
    if Vote.objects.filter(user=request.user, choice__poll=poll).exists():
        # User has already voted, redirect them to the view poll votes page
        return redirect('view_poll_votes', poll_id=poll_id)
    
    if request.method == 'POST':
        # Get the selected choice ID from the form data
        choice_id = request.POST.get('choice')
        try:
            # Retrieve the selected choice object
            selected_choice = poll.choice_set.get(pk=choice_id)
        except (KeyError, Choice.DoesNotExist):
            # If choice ID is not provided or choice does not exist, return to the poll detail page with an error message
            return render(request, 'vote_poll.html', {
                'poll': poll,
                'error_message': "Please select a valid choice.",
            })
        else:
            # Create a Vote object associating the current user and the selected choice
            Vote.objects.create(user=request.user, choice=selected_choice)
            
            # Increment the votes count for the selected choice
            selected_choice.votes += 1
            selected_choice.save()
            
            # Redirect to the view poll votes page after voting
            return redirect('view_poll_votes', poll_id=poll_id)
    return render(request, 'vote_poll.html', {'poll': poll})

@login_required
def view_poll_votes(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    total_votes = sum(choice.votes for choice in poll.choice_set.all())
    
    # Define a list of colors for the progress bars
    colors = ['#a7a7fe', '#f7b781', '#a7fef5', '#d4cf4c']  # Example colors
    
    # Calculate percentage for each choice and zip it with corresponding color
    choices_with_percentage_and_color = [
        (choice, (choice.votes / total_votes) * 100, colors[index % len(colors)]) 
        for index, choice in enumerate(poll.choice_set.all())
    ]
    
    return render(request, 'view_poll_votes.html', {'poll': poll,'total_votes':total_votes,'choices_with_percentage_and_color':choices_with_percentage_and_color})


def custom_logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def user_polls(request):
    user = request.user  # Assuming the user is authenticated
    user_polls = Poll.objects.filter(created_by=user)

    # Calculate total votes for each poll
    for poll in user_polls:
        poll.total_votes = sum(choice.votes for choice in poll.choice_set.all())

    return render(request, 'user_polls.html', {'user_polls': user_polls})


@login_required
def update_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id, created_by=request.user)  # Update this line
    choices = poll.choice_set.all()
    
    if request.method == 'POST':
        question = request.POST.get('question')
        choices_str = request.POST.get('choices')
        choice_texts = [choice.strip() for choice in choices_str.split(',') if choice.strip()]  # Split and strip choice texts
        
        if question and choices_str:
            poll.question = question
            poll.save()

            # Update existing choices or create new ones
            existing_choices_texts = list(choices.values_list('choice_text', flat=True))
            for choice_text in choice_texts:
                if choice_text in existing_choices_texts:
                    # Update existing choice
                    existing_choices_texts.remove(choice_text)  # This choice is still valid, remove from list to mark as updated
                else:
                    # Create new choice
                    Choice.objects.create(poll=poll, choice_text=choice_text)

            # Delete choices that were removed by the user
            choices.filter(choice_text__in=existing_choices_texts).delete()

            return redirect('user_polls')  # Redirect to a new URL

    # Prepopulate form with existing data
    existing_choices_str = ', '.join(choices.values_list('choice_text', flat=True))
    return render(request, 'update_poll.html', {'poll': poll, 'choices': choices})
