from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordResetForm, PasswordChangeForm
from django.utils.translation import gettext_lazy as _
from .models import User, Documento, Derivacion, Area, Respuesta, EstadoRespuesta, Perfil, TipoDocumento, TipoRemitente, Remitente

from datetime import date

class RegistrationForm(UserCreationForm):
  password1 = forms.CharField(
      label=_("Contraseña"),
      widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
  )
  password2 = forms.CharField(
      label=_("Confirmar Contraseña"),
      widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar Contraseña'}),
  )

  class Meta:
    model = User
    fields = ('username', 'email', )

    widgets = {
      'username': forms.TextInput(attrs={
          'class': 'form-control',
          'placeholder': 'Nombre de Usuario'
      }),
      'email': forms.EmailInput(attrs={
          'class': 'form-control',
          'placeholder': 'Correo'
      })
    }

class LoginForm(AuthenticationForm):
    username = UsernameField(
        label=_('Nombre de Usuario'),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )
    password = forms.CharField(
        label=_('Contraseña'),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
    )

class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))

class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        max_length=50, 
        widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Antigüa Contraseña'
    }), label='Antigüa Contraseña')
    new_password1 = forms.CharField(
        max_length=50, 
        widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Nueva Contraseña'
    }), label="Nueva Contraseña")
    new_password2 = forms.CharField(
        max_length=50, 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': 'Confirmar Nueva Contraseña'}), 
        label="Confirmar Nueva Contraseña")

class DocumentoForm(forms.ModelForm):
    perfil = forms.ModelChoiceField(queryset=Perfil.objects.all())
    #tipo_documento= forms.ModelChoiceField(queryset=TipoDocumento.objects.none())

    tipo_remitente = forms.ModelChoiceField(queryset=TipoRemitente.objects.all())
    #remitente = forms.ModelChoiceField(queryset=Remitente.objects.none())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'perfil' in self.data:
            try:
                perfil = Perfil
                perfil.id = int(self.data.get('perfil'))
                self.fields('tipo_documento').queryset = TipoDocumento.objects.filter(perfil.id).order_by('nombre')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['tipo_documento'].queryset = self.instance.perfil.tipo_documento
        
        if 'tipo_remitente' in self.data:
            try:
                tipoRemitente = TipoRemitente
                tipoRemitente.id = int(self.data.get('tipo_remitente'))
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['remitente'].queyset = self.instance.tipo_remitente.remitente

    today = date.today()

    fecha_recepcion = forms.DateField(
            label=_('Fecha de Recepción'),
            widget=forms.DateInput(attrs={
                'type': 'Date',
                'class': 'form-control',
                'value': today,
            })
    )
    fecha_emision = forms.DateField(
            label=_('Fecha de Emisión'),
            widget=forms.DateInput(attrs={
                'type': 'Date',
                'class': 'form-control',
                'value': today,
            })
    )    
    numero = forms.CharField(
        label=_('Número'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Número',
        })
    )    
    asunto = forms.CharField(
        label=_('Asunto'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Asunto',
        })
    )    
    descripcion =  forms.CharField(
        label=_('Descripción'),
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'placeholder': 'Descripción'}),
    )    

    class Meta:
        model= Documento
        fields= ['perfil','tipo_documento','tipo_remitente','remitente','fecha_recepcion','fecha_emision','numero','asunto','descripcion']

class DerivacionForm(forms.ModelForm):
    area_destino = forms.ModelChoiceField(
        label=_('Área'),
        queryset=Area.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    observacion = forms.CharField(
        label=_('Observación'),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Observaciones'}),
    )

    class Meta:
        model= Derivacion
        fields= ['area_destino', 'observacion']

class RespuestaForm(forms.ModelForm):
    estado = forms.ModelChoiceField(
        label=_('Estado'),
        queryset=EstadoRespuesta.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    observaciones = forms.CharField(
        label=_('Observación'),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Observaciones'}),
    )

    class Meta:
        model= Respuesta
        fields= ['estado', 'observaciones']

class RemitenteForm(forms.ModelForm):
    class Meta:
        model= Remitente
        fields= '__all__'