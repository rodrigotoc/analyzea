from django.contrib import admin

# Models
from .models import Area, PersonalArea, MesaPartes
from .models import TipoDocumento, Perfil, TipoRemitente, Remitente, Documento, EstadoTramite, Tramite, Respuesta, Derivacion, EstadoRespuesta
from .models import Pais, Ciudad

# Register your models here.
admin.site.register(Area)
admin.site.register(PersonalArea)
admin.site.register(MesaPartes)
admin.site.register(TipoDocumento)
admin.site.register(Perfil)
admin.site.register(TipoRemitente)
admin.site.register(Remitente)
admin.site.register(Documento)
admin.site.register(EstadoTramite)
admin.site.register(EstadoRespuesta)
admin.site.register(Tramite)
admin.site.register(Pais)
admin.site.register(Ciudad)
admin.site.register(Respuesta)
admin.site.register(Derivacion)