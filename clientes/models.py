from django.db import models
from django.core.validators import RegexValidator


class Cliente(models.Model):
    """
    Modelo para gestionar la información de clientes del estudio contable.
    """
    
    # Información básica
    nombre = models.CharField(
        max_length=200, 
        verbose_name="Nombre/Razón Social",
        help_text="Nombre completo o razón social del cliente"
    )
    
    cuit_validator = RegexValidator(
        regex=r'^\d{2}-\d{8}-\d{1}$',
        message='El CUIT debe tener el formato XX-XXXXXXXX-X'
    )
    cuit = models.CharField(
        max_length=13, 
        unique=True,
        validators=[cuit_validator],
        verbose_name="CUIT",
        help_text="CUIT en formato XX-XXXXXXXX-X"
    )
    
    domicilio = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Domicilio",
        help_text="Dirección completa del cliente"
    )
    
    # Claves de acceso a sistemas
    clave_fiscal = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name="Clave Fiscal",
        help_text="Clave de acceso a AFIP"
    )
    
    clave_ciudad = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name="Clave Ciudad",
        help_text="Clave de acceso a sistemas de CABA"
    )
    
    clave_arba = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name="Clave ARBA",
        help_text="Clave de acceso a ARBA"
    )
    
    clave_sec = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name="Clave SEC",
        help_text="Clave de acceso a SEC"
    )
    
    clave_faecys = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name="Clave FAECYS",
        help_text="Clave de acceso a FAECYS"
    )
    
    clave_inacap = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name="Clave INACAP",
        help_text="Clave de acceso a INACAP"
    )
    
    clave_osecac = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name="Clave OSECAC",
        help_text="Clave de acceso a OSECAC"
    )
    
    clave_rubrica_digital_caba = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name="Clave Rúbrica Digital CABA",
        help_text="Clave de acceso a Rúbrica Digital CABA"
    )
    
    clave_estudio_one_web = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name="Clave Estudio One Web",
        help_text="Clave de acceso a Estudio One Web"
    )
    
    # Información adicional
    registro_de_empleadores = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name="Registro de Empleadores",
        help_text="Número de registro de empleadores"
    )
    
    otros_datos = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Otros Datos",
        help_text="Información adicional del cliente"
    )
    
    # Información técnica/administrativa
    carpeta = models.CharField(
        max_length=200, 
        blank=True, 
        null=True,
        verbose_name="Carpeta",
        help_text="Ubicación de carpeta física o digital"
    )
    
    ptovta = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        verbose_name="Punto de Venta",
        help_text="Punto de venta asignado"
    )
    
    nombase = models.CharField(
        max_length=200, 
        blank=True, 
        null=True,
        verbose_name="Nombre Base",
        help_text="Nombre de base de datos"
    )
    
    ruta_base = models.CharField(
        max_length=500, 
        blank=True, 
        null=True,
        verbose_name="Ruta Base",
        help_text="Ruta de la base de datos"
    )
    
    rutabackup = models.CharField(
        max_length=500, 
        blank=True, 
        null=True,
        verbose_name="Ruta Backup",
        help_text="Ruta de respaldo"
    )
    
    # Campos de auditoría
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación"
    )
    
    fecha_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Modificación"
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si el cliente está activo"
    )

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nombre']
        
    def __str__(self):
        return f"{self.nombre} - {self.cuit}"
    
    def __repr__(self):
        return f"Cliente(pk={self.pk}, nombre='{self.nombre}', cuit='{self.cuit}')"
    
    @property
    def cuit_sin_guiones(self):
        """Retorna el CUIT sin guiones para uso en formularios AFIP"""
        return self.cuit.replace('-', '')
    
    @property
    def tiene_clave_fiscal(self):
        """Verifica si el cliente tiene clave fiscal configurada"""
        return bool(self.clave_fiscal and self.clave_fiscal.strip())
