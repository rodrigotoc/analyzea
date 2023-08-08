from django.contrib.auth.models import User
from django.db import models
import uuid

class Perfil(models.Model):
    nombre = models.CharField(max_length=50)
    # tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre

class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=50)
    perfil = models.ForeignKey(Perfil, on_delete=models.PROTECT)


    def __str__(self):
        return self.nombre

class TipoRemitente(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Pais(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Ciudad(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nombre}, {self.pais}'

class Remitente(models.Model):
    tipo_remitente = models.ForeignKey(TipoRemitente, on_delete=models.PROTECT)
    nombres = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)
    documento_identidad = models.CharField(max_length=15, null=True, blank=True)
    codigo_trabajador = models.CharField(max_length=15, null=True, blank=True)
    ruc = models.CharField(max_length=11, null=True, blank=True)
    razon_social = models.CharField(max_length=100, null=True, blank=True)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, null=True, blank=True)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.tipo_remitente} - {self.nombres}'

class Area(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Documento(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.PROTECT)
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.PROTECT)
    tipo_remitente = models.ForeignKey(TipoRemitente, on_delete=models.PROTECT)
    remitente = models.ForeignKey(Remitente, on_delete=models.PROTECT)
    fecha_recepcion = models.DateField()
    fecha_emision = models.DateField(null=True, blank=True)
    numero = models.CharField(max_length=50)
    asunto = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    fe_create = models.DateTimeField(auto_now_add=True)
    fe_update = models.DateTimeField(auto_now=True)   

    def __str__(self):
        return f'{self.numero} - {self.asunto}'  

class MesaPartes(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    documentos = models.ManyToManyField(Documento, through='Tramite')

    def __str__(self):
        return self.usuario.username

class PersonalArea(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.PROTECT)

    def __str__(self):
        return self.usuario.username

class Derivacion(models.Model):    
    area_destino = models.ForeignKey(Area, on_delete=models.PROTECT)
    mesa_partes = models.ForeignKey(MesaPartes, on_delete=models.PROTECT)
    observaciones = models.TextField(blank=True)
    fecha_create = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.area_destino} - {self.mesa_partes}'

class EstadoTramite(models.Model):
    descripcion = models.CharField(max_length=50)
    tramite_padre = models.IntegerField()

    def __str__(self):
        return self.descripcion

# class Cargo(models.Model):    
#     numero = models.CharField(max_length=50)
#     observaciones = models.TextField(blank=True)
#     fecha_create = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return self.numero

class Tramite(models.Model):
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE)
    numero_registro = models.IntegerField()
    mesa_partes = models.ForeignKey(MesaPartes, on_delete=models.CASCADE)    
    derivacion = models.ForeignKey(Derivacion, on_delete=models.PROTECT, null=True, blank=True)    
    observaciones = models.TextField(blank=True)
    estado_tramite = models.ForeignKey(EstadoTramite, on_delete=models.PROTECT)
    # cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT)
    fe_create = models.DateTimeField(auto_now_add=True)
    fe_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.documento.numero} - {self.mesa_partes.usuario.username}'
    
class Recepcion(models.Model):
    tramite = models.OneToOneField(Tramite, on_delete=models.CASCADE)
    personal_area = models.ForeignKey(PersonalArea, on_delete=models.PROTECT)
    observaciones = models.TextField(blank=True)
    fecha_create = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.tramite.documento.numero

class EstadoRespuesta(models.Model):
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion

class Respuesta(models.Model):
    tramite = models.OneToOneField(Tramite, on_delete=models.CASCADE)
    personal_area = models.ForeignKey(PersonalArea, on_delete=models.PROTECT)
    estado = models.ForeignKey(EstadoRespuesta, on_delete=models.CASCADE)
    observaciones = models.TextField(blank=True)
    fecha_create = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.tramite.documento.asunto
    
