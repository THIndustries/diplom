from django.views.generic import CreateView
from django.http import HttpResponse
from django.urls import reverse_lazy

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('index')
    template_name = 'mysiteapp/signup.html'


def index(request):
    return HttpResponse('My diplom work main page.')
