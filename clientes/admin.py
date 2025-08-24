from django.contrib import admin
from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Cliente.
    """
    
    list_display = [
        'nombre', 
        'cuit', 
        'domicilio', 
        'activo',
        'fecha_creacion'
    ]
    
    list_filter = [
        'activo', 
        'fecha_creacion', 
        'fecha_modificacion'
    ]
    
    search_fields = [
        'nombre', 
        'cuit', 
        'domicilio'
    ]
    
    list_editable = ['activo']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'cuit', 'domicilio', 'activo')
        }),
        ('Claves de Acceso', {
            'fields': (
                'clave_fiscal',
                'clave_ciudad', 
                'clave_arba',
                'clave_sec',
                'clave_faecys',
                'clave_inacap',
                'clave_osecac',
                'clave_rubrica_digital_caba',
                'clave_estudio_one_web'
            ),
            'classes': ('collapse',)
        }),
        ('Información Adicional', {
            'fields': (
                'registro_de_empleadores',
                'otros_datos'
            ),
            'classes': ('collapse',)
        }),
        ('Información Técnica', {
            'fields': (
                'carpeta',
                'ptovta',
                'nombase',
                'ruta_base',
                'rutabackup'
            ),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion', 'fecha_modificacion'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['fecha_creacion', 'fecha_modificacion']
    
    ordering = ['nombre']
    
    def get_readonly_fields(self, request, obj=None):
        """
        Hace que las fechas sean de solo lectura.
        """
        if obj:  # Editando un objeto existente
            return list(self.readonly_fields) + ['fecha_creacion']
        return self.readonly_fields
