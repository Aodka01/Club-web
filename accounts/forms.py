from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'carrera', 'semestre', 'area_maestro']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Verificar si el usuario es coordinador
        if self.user and self.user.groups.filter(name='Coordinador').exists():
            # Para coordinadores: mostrar solo área de maestro
            del self.fields['carrera']
            del self.fields['semestre']
            self.fields['area_maestro'].required = True
        else:
            # Para estudiantes: mostrar solo carrera y semestre
            del self.fields['area_maestro']
            self.fields['carrera'].required = True
            self.fields['semestre'].required = True