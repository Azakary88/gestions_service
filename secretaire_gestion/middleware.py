from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        login_url = reverse('login')

        # 🔥 Autoriser static (OBLIGATOIRE)
        if request.path.startswith('/static/'):
            return self.get_response(request)

        # Autoriser admin
        if request.path.startswith('/admin/'):
            return self.get_response(request)

        # 🔒 Bloquer si non connecté
        if not request.user.is_authenticated:
            if not request.path.startswith(login_url):
                return redirect('login')

        return self.get_response(request)