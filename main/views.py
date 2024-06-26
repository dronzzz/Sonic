from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    template = loader.get_template('index.html')
    # In your view
    print(request.user.is_authenticated)
    print(request.user.username)
    print(request.session.items())
    data = {
        "username": request.user.username,
    }

    # return HttpResponse(template.render({'request': request}))
    return HttpResponse(template.render({'data': data}, request))


@csrf_exempt
def search(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        token = getSpotifyAccessToken()
        list = requests.get(
            f"https://api.spotify.com/v1/search?q={query}&type=track&limit=5", headers={'Authorization': 'Bearer ' + token})
        print(list.json())
        return JsonResponse({'searchResults': list.json()})
    else:
        return JsonResponse({"message": "failed"})


def track(request, id):
    token = getSpotifyAccessToken()
    url = f"https://api.spotify.com/v1/tracks/{id}"
    headers = {'Authorization': 'Bearer ' + token}
    response = requests.get(url, headers=headers)
    context = response.json()
    print(context['name'])
    template = loader.get_template('track.html')
    return HttpResponse(template.render({'context': context}, request))


def getSpotifyAccessToken():
    url = "https://accounts.spotify.com/api/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": "f9257cdf01df46e69038ce898e4e14c4",
        "client_secret": "f97f24f668594b518b88fc81757e06b1"
    }
    response = requests.post(url, headers=headers, data=data)
    print(response.json())
    token = response.json()['access_token']
    return token


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to login page after successful registration
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})
