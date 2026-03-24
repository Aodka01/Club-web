from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'carrera', 'semestre', 'area_maestro']
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Cuéntanos un poco sobre ti...'}),
            'carrera': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Ingeniería en Sistemas'}),
            'semestre': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 12}),
            'area_maestro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Matemáticas, Física, etc.'}),
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