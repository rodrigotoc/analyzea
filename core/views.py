from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from core.forms import RegistrationForm, LoginForm, UserPasswordResetForm, UserPasswordChangeForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import MesaPartes, PersonalArea, EstadoTramite, Tramite, TipoDocumento, Perfil, Remitente
from .forms import DocumentoForm, DerivacionForm, RespuestaForm, RemitenteForm
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.http import JsonResponse
from django.db import connections
from django.db.models import Q

# Create your views here.
@login_required
def home(request):
    # print(request.user.groups.all())
    # print(request.user.pk)
    # print(request.user.groups.filter(name='Personal de Area').exists())

    # Logeo de Usuarios con grupo Mesa de Partes
    if request.user.groups.filter(name='Mesa de Partes').exists():
        mesa_partes = MesaPartes.objects.get(usuario=request.user)
        sidebar = 'Mesa de Partes'
        documentos_pendientes = mesa_partes.documentos.filter(tramite__derivacion=None)
        # print(documentos_pendientes)
        # print(request.POST)

        # documentos_asignados = mesa_partes.documentos.filter(tramite__asistente_area__isnull=False, tramite__fecha_recepcion=None)
        # context = {'documentos_pendientes': documentos_pendientes, 'documentos_asignados': documentos_asignados}
        # context = {'documentos_pendientes': documentos_pendientes}
        context = {'mesa_partes': mesa_partes,
                   'segment': 'index',
                   'sidebar': sidebar,
                   'documentos_pendientes': documentos_pendientes}
        return render(request, 'mesa_partes/home.html', context)
    elif request.user.groups.filter(name='Personal de Area').exists():
        personal_area = PersonalArea.objects.get(usuario=request.user)
        sidebar = 'Personal de Area'
        area = PersonalArea.objects.get(usuario=request.user).area
        # documentos_pendientes = Documento.objects.filter(area_destino=asistente_area.area, tramite__asistente_area=None)
        # documentos_asignados = Documento.objects.filter(area_destino=asistente_area.area, tramite__asistente_area=asistente_area, tramite__fecha_recepcion=None)
        # my_paginator = Paginator( documentos_pendientes, 3)
        # page_number = request.GET.get('page')
        # try:
        #     my_page = my_paginator.page(page_number)
        # except PageNotAnInteger:
        #     my_page = my_paginator.page(1)
        # except EmptyPage:
        #     my_page = my_paginator.page(my_paginator.num_pages)
        # context = {'asistente_area': asistente_area,'documentos_pendientes': documentos_pendientes, 'documentos_asignados': documentos_asignados, 'my_page': my_page}
        context = {'personal_area': personal_area,
                   'segment': 'index',
                   'area': area,
                   'sidebar': sidebar}
        return render(request, 'areas/home.html', context)
    elif request.user.is_superuser:
        return redirect('admin:index')
    else:
        return redirect('login')

@login_required
def registrar_documento(request):
  if request.method == 'POST':
    form = DocumentoForm(request.POST)
    print(form)
    print(request.POST)
    print(form.errors)
    if form.is_valid():
      documento = form.save()
      print('Registro creado con éxito!')
      # Recuperar el numero del registro
      ultimo_registro = Tramite.objects.latest('fe_create')
      valor_num_registro = ultimo_registro.numero_registro
      num_registro_actual = valor_num_registro + 1
      nuevo_tramite = Tramite(
        documento = documento,
        numero_registro = num_registro_actual,
        mesa_partes = MesaPartes.objects.get(usuario=request.user),
        estado_tramite = EstadoTramite.objects.get(descripcion='Registrado')
      )
      nuevo_tramite.save()
      return redirect('listar_documentos_registrados')
    else:
      print('El registro no fue creado!')
  else:
    form = DocumentoForm

  context = {'segment': 'registrar_documento',
              'form': form,
              'sidebar': 'Mesa de Partes'
            }
  template = 'mesa_partes/registrar_documento.html'

  return render(request, template, context)

@login_required
def cargar_tipo_documento(request):
    perfil = request.GET.get('perfil')
    print(perfil)
    tipo_documento = TipoDocumento.objects.filter(perfil_id=perfil).order_by('nombre')
    print(tipo_documento)
    return JsonResponse(list(tipo_documento.values('id', 'nombre')), safe=False)

@login_required
def cargar_remitente(request):
    tipo_remitente = request.GET.get('remitente')
    print(tipo_remitente)
    remitente = Remitente.objects.filter(tipo_remitente_id=tipo_remitente).order_by('nombres')      
    return JsonResponse(list(remitente.values('id', 'nombres')), safe=False)

@login_required
def listar_documentos_registrados(request):
  # Recuperar tramites registrados
  tramites_registrados = Tramite.objects.filter(estado_tramite__descripcion='Registrado').order_by('-documento__fecha_recepcion')

  context = {'segment': 'listar_documentos_registrados',
              'sidebar': 'Mesa de Partes',
              'tramites_registrados': tramites_registrados
            }
  template = 'mesa_partes/listar_documentos_registrados.html'

  return render(request, template, context)

@login_required
def derivar_tramite(request, id):
  # Recuperar tramite por ID
   tramite = get_object_or_404(Tramite, pk=id)

   # Verificar que el tramite no haya sido derivado anteriormente
   # 1 = Registrado
   if tramite.estado_tramite.pk != 1:
      return redirect('404_error')

   if request.method == 'POST':
      form = DerivacionForm(request.POST)
      print(form)
      print(request.POST)
      if form.is_valid():
         derivacion = form.save(commit=False)
         derivacion.mesa_partes = MesaPartes.objects.get(usuario=request.user)
         derivacion = form.save()
         print('Derivación creada con éxito!')
         tramite.derivacion = derivacion
         tramite.estado_tramite = EstadoTramite.objects.get(descripcion='Derivado')
         tramite.save()
         return redirect('listar_documentos_registrados')
      else:
         print('El registro no fue creado!')
   else:
     form = DerivacionForm(instance=tramite)


   context = {'segment': 'derivar_tramite',
              'sidebar': 'Mesa de Partes',
              'tramite': tramite,
              'form': form,
              }
   template = 'mesa_partes/derivar_tramite.html'
   return render(request, template, context)

@login_required
def ver_tramite(request,id):
  tramite = get_object_or_404(Tramite, pk=id)

   # Verificar que el tramite no haya sido derivado anteriormente
   # 1 = Registrado
  # if tramite.estado_tramite.pk != 1:
  #   return redirect('404_error')

  context = {'segment': 'ver_tramite',
              'sidebar': 'Mesa de Partes',
              'tramite': tramite,
            }
  template = 'mesa_partes/ver_tramite.html'
  return render(request, template, context)

@login_required
def error_404(request):
   context = {}
   template = 'pages/404_error.html'
   return render(request,template, context)


@login_required
def listar_todos_tramites(request):
  # Recuperar todos los tramites
  # Mejora: Recuperar y separar todos los tramites con estado 'En tramite' 'Finalizado'
  todos_tramites = Tramite.objects.all().order_by('-documento__fecha_recepcion')

  context = {'segment': 'listar_todos_tramites',
             'sidebar': 'Mesa de Partes',
             'tramites': todos_tramites,
            }
  template = 'mesa_partes/listar_todos_tramites.html'
  return render(request, template, context)

@login_required
def tramites_recibidos(request):
  # Recuperar area del asistente registrado
  areaUsuario = PersonalArea.objects.get(usuario=request.user).area.pk

  # Recupera tramites recibidos segun el area del usuario
  tramites_area = Tramite.objects.filter(derivacion__area_destino=areaUsuario)
  tramites_recibidos = tramites_area.filter(estado_tramite__descripcion='Derivado').order_by('-documento__fecha_recepcion')
  sidebar = 'Personal de Area'

  context = {'segment': 'tramites_recibidos',
             'sidebar': sidebar,
             'tramites_recibidos': tramites_recibidos,
              }
  template = 'areas/tramites_recibidos.html'
  return render(request, template, context)

@login_required
def tramites_aceptados(request):
  # Recuperar area del asistente registrado
  areaUsuario = PersonalArea.objects.get(usuario=request.user).area.pk

  # Recupera tramites recibidos segun el area del usuario
  tramites_area = Tramite.objects.filter(derivacion__area_destino=areaUsuario)
  tramites_aceptados = tramites_area.filter(estado_tramite__descripcion='Recibido').order_by('-documento__fecha_recepcion')
  sidebar = 'Personal de Area'

  context = {'segment': 'tramites_aceptados',
             'sidebar': sidebar,
             'tramites_aceptados': tramites_aceptados,
              }
  template = 'areas/tramites_aceptados.html'
  return render(request, template, context)

@login_required
def responder_tramite(request, id):
  # Recuperar tramite por ID
  tramite = get_object_or_404(Tramite, pk=id)

  if request.method == 'POST':
    form = RespuestaForm(request.POST)

    if form.is_valid():
        respuesta = form.save(commit=False)
        respuesta.personal_area = PersonalArea.objects.get(usuario=request.user)
        respuesta.tramite = tramite
        respuesta = form.save()
        if respuesta.estado.descripcion == 'Aceptado':
          tramite.estado_tramite = EstadoTramite.objects.get(descripcion='Recibido')
          tramite.save()
        elif respuesta.estado.descripcion == 'Rechazado':
          tramite.estado_tramite = EstadoTramite.objects.get(descripcion='Rechazado')
          tramite.save()
        print('Se guardo la respuesta exitosamente!')
        return redirect('tramites_aceptados')
    else:
      print('No se guardó la respuesta!')
  else:
     form = RespuestaForm(instance=tramite)

  sidebar = 'Personal de Area'

  context = {'segment': 'responder_tramite',
             'sidebar': sidebar,
             'tramite': tramite,
             'form':form
            }
  template = 'areas/responder_tramite.html'
  return render(request, template, context)

@login_required
def listar_tramites_rechazados (request):
  # Recuperar todos los documentos con estado rechazado
  tramites_rechazados = Tramite.objects.filter(estado_tramite__descripcion='Rechazado').order_by('-documento__fecha_recepcion')

  context = {'segment': 'listar_tramites_rechazados',
              'sidebar': 'Mesa de Partes',
              'tramites_rechazados': tramites_rechazados,
            }
  template = 'mesa_partes/listar_tramites_rechazados.html'

  return render(request, template, context)

@login_required
def crear_remitente (request):
  if request.method == 'POST':
    form = RemitenteForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('registrar_documento')
        # hacer algo después de guardar los datos del usuario
  else:
    form = RemitenteForm()
  context = {'segment': 'crear_remitente',
            'sidebar': 'Mesa de Partes',
            'form': form,       
            }
  
  template = 'mesa_partes/crear_remitente.html'

  return render(request, template, context)


#Authentication
class UserLoginView(LoginView):
   template_name = 'accounts/login.html'
   form_class = LoginForm

   def form_valid(self, form):
      # Redirige al usuario a la página de inicio después de iniciar sesión correctamente.
      response = super().form_valid(form)
      return response

@login_required
def profile(request):
  if request.user.groups.filter(name='Mesa de Partes').exists():
    sidebar = 'Mesa de Partes'
    context = {'segment': 'profile',
               'sidebar': sidebar}
    template = 'accounts/profile.html'
    return render(request, template, context)

  elif request.user.groups.filter(name='Personal de Area').exists():
    sidebar = 'Personal de Area'
    context = {'segment': 'profile',
               'sidebar': sidebar}
    template = 'accounts/profile.html'
    return render(request, template, context)

@login_required
def register(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      form.save()
      print('Cuenta creada satisfactoriamente!')
      return redirect('/accounts/login/')
    else:
      print("Register failed!")
  else:
    form = RegistrationForm()

  context = { 'form': form }
  return render(request, 'accounts/register.html', context)

@login_required
def logout_view(request):
  logout(request)
  return redirect('/accounts/login/')

class UserPasswordResetView(PasswordResetView):
  template_name = 'accounts/password_reset.html'
  form_class = UserPasswordResetForm

class UserPasswordChangeView(PasswordChangeView):
  template_name = 'accounts/password_change.html'
  form_class = UserPasswordChangeForm