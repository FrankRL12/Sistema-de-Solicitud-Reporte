from django.shortcuts import redirect
from django.urls import reverse

class PostLoginRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Verifica si el usuario está autenticado
        if request.user.is_authenticated:
            # Redirige a la vista 'dashboard' si el usuario es 'admin'
            if request.user.username == 'admin' and request.path == reverse('login'):
                return redirect('dashboard')  # Reemplaza 'dashboard' con el nombre de la vista correspondiente
            # Redirige a la vista 'inicio' para usuarios normales
            elif request.path == reverse('login'):
                return redirect('inicio')  # Reemplaza 'inicio' con el nombre de la vista correspondiente

        return response
