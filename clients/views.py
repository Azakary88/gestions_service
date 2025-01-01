from django.shortcuts import render, redirect
from .forms import ClientForm
from .models import Client

def ajouter_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_clients')
    else:
        form = ClientForm()
    return render(request, 'clients/ajouter_client.html', {'form': form})

def liste_clients(request):
    clients = Client.objects.all()
    return render(request, 'clients/liste_clients.html', {'clients': clients})
