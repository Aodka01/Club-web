from django import forms
from .models import Event, EventComment


class EventForm(forms.ModelForm):
    """Formulario mejorado para crear/editar eventos"""
    
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        label='Fecha del Evento'
    )
    
    hora = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control'
        }),
        label='Hora del Evento'
    )
    
    class Meta:
        model = Event
        fields = ['titulo', 'descripcion', 'lugar', 'cupo', 'foto']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Reunión de bienvenida'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe qué va a ocurrir en el evento...'
            }),
            'lugar': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Salón A, Patio principal'
            }),
            'cupo': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Máximo de personas (opcional)'
            }),
            'foto': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si estamos editando un evento, desglosa la fecha_hora en fecha y hora
        if self.instance.pk and self.instance.fecha_hora:
            self.fields['fecha'].initial = self.instance.fecha_hora.date()
            self.fields['hora'].initial = self.instance.fecha_hora.time()
    
    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')
        
        if fecha and hora:
            from datetime import datetime
            from django.utils import timezone
            
            # Combinar fecha y hora en un datetime
            dt = datetime.combine(fecha, hora)
            # Hacerlo timezone-aware
            dt = timezone.make_aware(dt, timezone.get_current_timezone())
            cleaned_data['fecha_hora'] = dt
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        # Usar la fecha_hora combinada del cleaned_data
        instance.fecha_hora = self.cleaned_data.get('fecha_hora')
        if commit:
            instance.save()
        return instance


class EventCommentForm(forms.ModelForm):
    """Formulario para comentarios en eventos"""
    
    class Meta:
        model = EventComment
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Comparte tu comentario...'
            })
        }
