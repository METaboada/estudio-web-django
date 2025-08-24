from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Cliente
from .serializers import (
    ClienteSerializer, 
    ClienteListSerializer, 
    ClienteCreateSerializer,
    ClienteUpdateSerializer
)


# ====== VISTAS WEB (TRADICIONALES) ======

def lista_clientes(request):
    """
    Vista web para mostrar la lista de clientes.
    """
    search_query = request.GET.get('search', '')
    activo_filter = request.GET.get('activo', '')
    
    clientes = Cliente.objects.all()
    
    # Aplicar filtros
    if search_query:
        clientes = clientes.filter(
            Q(nombre__icontains=search_query) |
            Q(cuit__icontains=search_query) |
            Q(domicilio__icontains=search_query)
        )
    
    if activo_filter:
        clientes = clientes.filter(activo=activo_filter == 'true')
    
    clientes = clientes.order_by('nombre')
    
    # Paginación
    paginator = Paginator(clientes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'activo_filter': activo_filter,
    }
    
    return render(request, 'clientes/lista.html', context)


def detalle_cliente(request, pk):
    """
    Vista web para mostrar el detalle de un cliente.
    """
    cliente = get_object_or_404(Cliente, pk=pk)
    
    context = {
        'cliente': cliente,
    }
    
    return render(request, 'clientes/detalle.html', context)


def crear_cliente(request):
    """
    Vista web para crear un nuevo cliente.
    """
    if request.method == 'POST':
        try:
            # Crear nuevo cliente con los datos del formulario
            cliente = Cliente.objects.create(
                cuit=request.POST.get('cuit', ''),
                nombre=request.POST.get('razon_social', ''),
                nombre_fantasia=request.POST.get('nombre_fantasia', ''),
                condicion_iva=request.POST.get('condicion_iva', ''),
                domicilio=request.POST.get('domicilio', ''),
                localidad=request.POST.get('localidad', ''),
                provincia=request.POST.get('provincia', ''),
                codigo_postal=request.POST.get('codigo_postal', ''),
                telefono=request.POST.get('telefono', ''),
                email=request.POST.get('email', ''),
                clave_fiscal=request.POST.get('clave_fiscal', ''),
                clave_certificado=request.POST.get('clave_certificado', ''),
                observaciones=request.POST.get('observaciones', ''),
                estado=request.POST.get('estado', 'ACTIVO')
            )
            
            messages.success(request, f'Cliente {cliente.nombre} creado exitosamente.')
            return redirect('clientes:lista')
            
        except Exception as e:
            messages.error(request, f'Error al crear cliente: {str(e)}')
    
    return render(request, 'clientes/crear.html')


def editar_cliente(request, pk):
    """
    Vista web para editar un cliente existente.
    """
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        # Aquí procesaríamos la actualización
        pass
    
    context = {
        'cliente': cliente,
    }
    
    return render(request, 'clientes/editar.html', context)


@require_http_methods(["POST"])
def eliminar_cliente(request, pk):
    """
    Vista web para eliminar un cliente (AJAX).
    """
    try:
        cliente = get_object_or_404(Cliente, pk=pk)
        cliente.delete()
        return JsonResponse({
            'success': True,
            'message': f'Cliente {cliente.nombre} eliminado correctamente.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al eliminar cliente: {str(e)}'
        }, status=400)


# ====== VISTAS API REST ======

class ClienteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para la API REST de clientes.
    
    Proporciona operaciones CRUD completas para clientes:
    - GET /api/clientes/ - Lista todos los clientes
    - POST /api/clientes/ - Crea un nuevo cliente
    - GET /api/clientes/{id}/ - Obtiene un cliente específico
    - PUT /api/clientes/{id}/ - Actualiza un cliente completo
    - PATCH /api/clientes/{id}/ - Actualiza parcialmente un cliente
    - DELETE /api/clientes/{id}/ - Elimina un cliente
    """
    
    queryset = Cliente.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """
        Retorna el serializer apropiado según la acción.
        """
        if self.action == 'list':
            return ClienteListSerializer
        elif self.action == 'create':
            return ClienteCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ClienteUpdateSerializer
        return ClienteSerializer
    
    def get_queryset(self):
        """
        Filtra los clientes según los parámetros de consulta.
        """
        queryset = Cliente.objects.all()
        
        # Filtro por búsqueda
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) |
                Q(cuit__icontains=search) |
                Q(domicilio__icontains=search)
            )
        
        # Filtro por estado activo
        activo = self.request.query_params.get('activo', None)
        if activo is not None:
            queryset = queryset.filter(activo=activo.lower() == 'true')
        
        return queryset.order_by('nombre')
    
    @action(detail=True, methods=['post'])
    def toggle_activo(self, request, pk=None):
        """
        Acción personalizada para cambiar el estado activo/inactivo de un cliente.
        """
        cliente = self.get_object()
        cliente.activo = not cliente.activo
        cliente.save()
        
        serializer = self.get_serializer(cliente)
        return Response({
            'message': f'Cliente {"activado" if cliente.activo else "desactivado"} correctamente',
            'cliente': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def buscar_por_cuit(self, request):
        """
        Busca un cliente por CUIT exacto.
        """
        cuit = request.query_params.get('cuit', None)
        if not cuit:
            return Response(
                {'error': 'El parámetro CUIT es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            cliente = Cliente.objects.get(cuit=cuit)
            serializer = self.get_serializer(cliente)
            return Response(serializer.data)
        except Cliente.DoesNotExist:
            return Response(
                {'error': 'Cliente no encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """
        Retorna estadísticas básicas de clientes.
        """
        total_clientes = Cliente.objects.count()
        clientes_activos = Cliente.objects.filter(activo=True).count()
        clientes_inactivos = total_clientes - clientes_activos
        clientes_con_clave_fiscal = Cliente.objects.exclude(
            Q(clave_fiscal__isnull=True) | Q(clave_fiscal='')
        ).count()
        
        return Response({
            'total_clientes': total_clientes,
            'clientes_activos': clientes_activos,
            'clientes_inactivos': clientes_inactivos,
            'clientes_con_clave_fiscal': clientes_con_clave_fiscal,
            'porcentaje_activos': round((clientes_activos / total_clientes * 100), 2) if total_clientes > 0 else 0,
        })
