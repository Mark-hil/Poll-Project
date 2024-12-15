from django.http import HttpResponse
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CreatePollForm
from .models import Poll
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
import matplotlib.pyplot as plt
import io
import urllib, base64

def home(request):
    polls = Poll.objects.all()
    context = {
        'polls': polls
    }
    return render(request, 'poll/home.html', context)

def create(request):
    if request.method == 'POST':
        form = CreatePollForm(request.POST)
        if form.is_valid():
            # print (form.cleaned_data['question'])
            form.save()
            return redirect('home')
    else:
        form = CreatePollForm()
    context = {
            'form' : form
        }
    return render(request, 'poll/create.html', context)

@login_required
def vote(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    if request.method == 'POST':
        selected_option = request.POST['poll']
        if selected_option == 'option1':
            poll.option_one_count += 1
        elif selected_option == 'option2':
            poll.option_two_count += 1
        elif selected_option == 'option3':
            poll.option_three_count += 1
        else: 
            return HttpResponse(400,'invalid forms')
        
        poll.save()
        
        return redirect('home')
        
    context = {
        'poll' : poll
    }
    return render(request, 'poll/vote.html', context)

def results(request,poll_id):
    poll = Poll.objects.get(pk=poll_id)
    context = {
        'poll' : poll
    }
    return render(request, 'poll/results.html', context)



@login_required
def delete_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if request.method == "POST":
        if "confirm" in request.POST:
            poll.delete()
            return redirect('home')
        else:
            return redirect('home')
    return render(request, 'poll/delete_poll.html', {'poll': poll})


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'poll/login.html', {'error': 'Invalid username or password'})
    return render(request, 'poll/login.html')

def user_logout(request):
    logout(request)
    return redirect('home')



import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import io
import urllib, base64
from django.shortcuts import render
from .models import Poll

def all_results(request):
    polls = Poll.objects.all()
    poll_results = []
    graph_uris = []
    
    for poll in polls:
        total_votes = poll.option_one_count + poll.option_two_count + poll.option_three_count
        poll_results.append({
            'question': poll.question,
            'option_one': poll.option_one,
            'option_two': poll.option_two,
            'option_three': poll.option_three,
            'option_one_count': poll.option_one_count,
            'option_two_count': poll.option_two_count,
            'option_three_count': poll.option_three_count,
            'total_votes': total_votes
        })

        # Generate the plot using Seaborn
        sns.set(style="whitegrid")
        plt.figure(figsize=(8, 6))
        
        labels = ['Option 1', 'Option 2', 'Option 3']
        votes = [poll.option_one_count, poll.option_two_count, poll.option_three_count]
        
        sns.barplot(x=labels, y=votes, palette='viridis')
        plt.xlabel('Options', fontweight='bold')
        plt.ylabel('Votes', fontweight='bold')
        plt.title(f'Results for: {poll.question}')
        
        # Save the plot to a PNG image
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)
        graph_uris.append(uri)

    results_with_graphs = zip(poll_results, graph_uris)

    context = {
        'results_with_graphs': results_with_graphs,
    }
    return render(request, 'poll/all_results.html', context)
