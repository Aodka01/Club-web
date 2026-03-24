from django.views.generic import ListView, DetailView
from .models import Club
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Club, Membership, Event, EventComment, EventAttendance
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import View
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django import forms
from .forms import ClubForm, EventForm, EventCommentForm


class ClubListView(LoginRequiredMixin, ListView):
    model = Club
    template_name = 'clubs/club_list.html'
    context_object_name = 'clubs'
    login_url = 'login'  # redirige al login si no está autenticado

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['es_coordinador'] = self.request.user.groups.filter(name="Coordinador").exists()
        # Agregar list de clubes en los que el usuario está inscrito
        context['mis_clubes'] = Membership.objects.filter(user=self.request.user).values_list('club_id', flat=True)
        return context


class ClubDetailView(LoginRequiredMixin, DetailView):
    """Vista de detalle para que estudiantes vean info del club sin poder editar"""
    model = Club
    template_name = 'clubs/club_detail.html'
    context_object_name = 'club'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['es_coordinador'] = self.request.user.groups.filter(name="Coordinador").exists()
        context['es_creador'] = self.object.creado_por == self.request.user
        context['ya_inscrito'] = Membership.objects.filter(user=self.request.user, club=self.object).exists()
        return context


class ClubCreateView(LoginRequiredMixin, UserPassesTestMixin,CreateView):
    model = Club
    form_class = ClubForm
    template_name = 'clubs/club_form.html'
    success_url = reverse_lazy('club_list')

    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.groups.filter(name="Coordinador").exists()

    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        return super().form_valid(form)


class ClubUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Club
    form_class = ClubForm
    template_name = 'clubs/club_form.html'
    success_url = reverse_lazy('club_list')

    def test_func(self):
        club = self.get_object()
        # Coordinador puede editar cualquier club, creador puede editar los suyos
        es_coordinador = self.request.user.groups.filter(name="Coordinador").exists()
        es_creador = club.creado_por == self.request.user
        return es_coordinador or es_creador


class ClubDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Club
    template_name = 'clubs/club_confirm_delete.html'
    success_url = reverse_lazy('club_list')

    def test_func(self):
        club = self.get_object()
        # Coordinador puede eliminar cualquier club, creador puede eliminar los suyos
        es_coordinador = self.request.user.groups.filter(name="Coordinador").exists()
        es_creador = club.creado_por == self.request.user
        return es_coordinador or es_creador


@method_decorator(login_required, name='dispatch')
class JoinClubView(View):
    def post(self, request, pk):
        try:
            club = Club.objects.get(pk=pk)
        except Club.DoesNotExist:
            raise Http404("Club no encontrado")
        
        # Crear membresía si no existe
        membership, created = Membership.objects.get_or_create(
            user=request.user,
            club=club
        )
        
        if created:
            from django.contrib import messages
            messages.success(request, f'Te has unido al club "{club.nombre}" exitosamente.')
            # Notificar al creador del club si existe
            if club.creado_por and club.creado_por != request.user:
                # Aquí podrías enviar un email o guardar una notificación en BD
                # Por simplicidad, solo mensaje para el usuario
                pass
        
        return redirect('club_detail', pk=pk)


@method_decorator(login_required, name='dispatch')
class RemoveMemberView(View):
    """Vista para que coordinador/creador elimine a un miembro del club"""
    def post(self, request, club_pk, member_pk):
        try:
            club = Club.objects.get(pk=club_pk)
            membership = Membership.objects.get(pk=member_pk, club=club)
        except (Club.DoesNotExist, Membership.DoesNotExist):
            raise Http404("Club o miembro no encontrado")
        
        # Validar que coordinador o creador del club puede eliminar miembros
        es_coordinador = request.user.groups.filter(name="Coordinador").exists()
        es_creador = club.creado_por == request.user
        
        if not (es_coordinador or es_creador):
            raise Http404("No tienes permiso para eliminar miembros")
        
        membership.delete()
        return redirect('club_detail', pk=club_pk)


@method_decorator(login_required, name='dispatch')
class LeaveClubView(View):
    """Vista para que un estudiante se salga del club"""
    def post(self, request, club_pk):
        try:
            club = Club.objects.get(pk=club_pk)
            membership = Membership.objects.get(user=request.user, club=club)
        except (Club.DoesNotExist, Membership.DoesNotExist):
            raise Http404("Club o membresía no encontrada")
        
        membership.delete()
        return redirect('club_list')


# ==================== VISTAS DE EVENTOS ====================

class EventListView(LoginRequiredMixin, ListView):
    """Lista de eventos de un club"""
    model = Event
    template_name = 'clubs/event_list.html'
    context_object_name = 'events'
    login_url = 'login'

    def get_queryset(self):
        club_pk = self.kwargs['club_pk']
        return Event.objects.filter(club_id=club_pk).order_by('-fecha_hora')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['club'] = Club.objects.get(pk=self.kwargs['club_pk'])
        context['es_coordinador'] = self.request.user.groups.filter(name="Coordinador").exists()
        return context


class EventDetailView(LoginRequiredMixin, DetailView):
    """Detalle del evento con comentarios"""
    model = Event
    template_name = 'clubs/event_detail.html'
    context_object_name = 'event'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['es_coordinador'] = self.request.user.groups.filter(name="Coordinador").exists()
        context['es_creador'] = self.object.creado_por == self.request.user
        context['comentarios'] = self.object.comentarios.all()
        context['esta_inscrito'] = EventAttendance.objects.filter(event=self.object, user=self.request.user).exists()
        context['asistentes'] = EventAttendance.objects.filter(event=self.object).select_related('user__profile')
        context['cupo_disponible'] = self.object.cupo and (self.object.cupo - context['asistentes'].count()) if self.object.cupo else None
        return context


class EventCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Crear evento (solo coordinador)"""
    model = Event
    form_class = EventForm
    template_name = 'clubs/event_form.html'

    def test_func(self):
        return self.request.user.groups.filter(name="Coordinador").exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['club'] = Club.objects.get(pk=self.kwargs['club_pk'])
        return context

    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        form.instance.club_id = self.kwargs['club_pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('event_list', kwargs={'club_pk': self.object.club.pk})


class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Editar evento (solo coordinador o creador)"""
    model = Event
    form_class = EventForm
    template_name = 'clubs/event_form.html'

    def test_func(self):
        event = self.get_object()
        es_coordinador = self.request.user.groups.filter(name="Coordinador").exists()
        es_creador = event.creado_por == self.request.user
        return es_coordinador or es_creador

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['club'] = self.object.club
        return context

    def get_success_url(self):
        return reverse_lazy('event_detail', kwargs={'pk': self.object.pk})


class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Eliminar evento (solo coordinador o creador)"""
    model = Event
    template_name = 'clubs/event_confirm_delete.html'

    def test_func(self):
        event = self.get_object()
        es_coordinador = self.request.user.groups.filter(name="Coordinador").exists()
        es_creador = event.creado_por == self.request.user
        return es_coordinador or es_creador

    def get_success_url(self):
        return reverse_lazy('event_list', kwargs={'club_pk': self.object.club.pk})


@method_decorator(login_required, name='dispatch')
class AddCommentView(View):
    """Agregar comentario a un evento"""
    def post(self, request, event_pk):
        event = get_object_or_404(Event, pk=event_pk)
        contenido = request.POST.get('contenido', '').strip()
        
        if contenido:
            EventComment.objects.create(
                event=event,
                usuario=request.user,
                contenido=contenido
            )
        
        return redirect('event_detail', pk=event_pk)


@method_decorator(login_required, name='dispatch')
class DeleteCommentView(View):
    """Eliminar comentario (solo el autor o coordinador)"""
    def post(self, request, comment_pk):
        comment = get_object_or_404(EventComment, pk=comment_pk)
        event_pk = comment.event.pk
        
        es_coordinador = request.user.groups.filter(name="Coordinador").exists()
        es_autor = comment.usuario == request.user
        
        if not (es_coordinador or es_autor):
            raise Http404("No tienes permiso para eliminar este comentario")
        
        comment.delete()
        return redirect('event_detail', pk=event_pk)


@method_decorator(login_required, name='dispatch')
class JoinEventView(View):
    """Inscribirse a un evento"""
    def post(self, request, event_pk):
        try:
            event = Event.objects.get(pk=event_pk)
        except Event.DoesNotExist:
            raise Http404("Evento no encontrado")
        
        # Verificar si ya está inscrito
        if EventAttendance.objects.filter(event=event, user=request.user).exists():
            from django.contrib import messages
            messages.warning(request, 'Ya estás inscrito en este evento.')
            return redirect('event_detail', pk=event_pk)
        
        # Verificar cupo si existe
        if event.cupo:
            current_attendees = EventAttendance.objects.filter(event=event).count()
            if current_attendees >= event.cupo:
                from django.contrib import messages
                messages.error(request, 'El evento ya está lleno. No hay cupo disponible.')
                return redirect('event_detail', pk=event_pk)
        
        # Crear asistencia
        EventAttendance.objects.create(event=event, user=request.user)
        
        from django.contrib import messages
        messages.success(request, f'Te has inscrito exitosamente al evento "{event.titulo}".')
        
        return redirect('event_detail', pk=event_pk)


@method_decorator(login_required, name='dispatch')
class LeaveEventView(View):
    """Desinscribirse de un evento"""
    def post(self, request, event_pk):
        try:
            event = Event.objects.get(pk=event_pk)
            attendance = EventAttendance.objects.get(event=event, user=request.user)
        except (Event.DoesNotExist, EventAttendance.DoesNotExist):
            raise Http404("Evento o asistencia no encontrada")
        
        attendance.delete()
        
        from django.contrib import messages
        messages.success(request, f'Te has desinscrito del evento "{event.titulo}".')
        
        return redirect('event_detail', pk=event_pk)
