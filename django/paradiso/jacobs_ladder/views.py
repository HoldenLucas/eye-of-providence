from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, "jacobs_ladder/index.html")
