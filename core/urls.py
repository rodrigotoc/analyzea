from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    #Mesa de Partes
    path('', views.home, name='home'),
    path('registrar-documento', views.registrar_documento, name='registrar_documento'),
    path('cargar-tipo-documento/', views.cargar_tipo_documento, name='cargar_tipo_documento'),
    path('cargar-remitente/', views.cargar_remitente, name="cargar_remitente"),
    path('listar-documentos-registrados', views.listar_documentos_registrados, name='listar_documentos_registrados'),
    path('derivar_tramite/<int:id>/',views.derivar_tramite, name='derivar_tramite'),
    path('listar-todos-tramites', views.listar_todos_tramites, name='listar_todos_tramites'),    
    path('listar-tramites-rechazados', views.listar_tramites_rechazados, name='listar_tramites_rechazados'),    
    path('404/', views.error_404, name = '404_error'),
    path('ver_tramite/<int:id>/', views.ver_tramite, name='ver_tramite'),
    path('crear_remitente', views.crear_remitente, name='crear_remitente'),
    
    #Area
    path('tramites-recibidos', views.tramites_recibidos, name='tramites_recibidos'),
    path('tramites-aceptados', views.tramites_aceptados, name='tramites_aceptados'),
    path('responder_tramite/<int:id>/', views.responder_tramite, name='responder_tramite'),

    #Accounts
    path('accounts/profile/', views.profile, name='profile'),

    #Authentication
    path('accounts/login/', views.UserLoginView.as_view(), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/password-change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('accounts/password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'
    ), name="password_change_done"),
    path('accounts/password-reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
]    