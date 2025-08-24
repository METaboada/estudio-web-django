from django.shortcuts import render
from clientes.models import Cliente


def home_view(request):
    """
    Vista principal del estudio contable.
    Muestra un dashboard con estadísticas y accesos rápidos.
    """
    # Estadísticas básicas
    total_clientes = Cliente.objects.count()
    clientes_activos = Cliente.objects.filter(activo=True).count()
    clientes_inactivos = total_clientes - clientes_activos
    
    context = {
        'total_clientes': total_clientes,
        'clientes_activos': clientes_activos,
        'clientes_inactivos': clientes_inactivos,
    }
    
    return render(request, 'home/index.html', context)
