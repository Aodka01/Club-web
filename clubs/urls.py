from django.urls import path
from .views import (ClubListView, ClubCreateView, ClubUpdateView, ClubDeleteView, JoinClubView, ClubDetailView, 
                    RemoveMemberView, LeaveClubView, EventListView, EventDetailView, EventCreateView, 
                    EventUpdateView, EventDeleteView, AddCommentView, DeleteCommentView)

urlpatterns = [
    path('', ClubListView.as_view(), name='club_list'),   # raíz de la app clubs
    path('add/', ClubCreateView.as_view(), name='club_add'),
    path('<int:pk>/', ClubDetailView.as_view(), name='club_detail'),
    path('<int:pk>/edit/', ClubUpdateView.as_view(), name='club_edit'),
    path('<int:pk>/delete/', ClubDeleteView.as_view(), name='club_delete'),
    path('<int:pk>/join/', JoinClubView.as_view(), name='club_join'),
    path('<int:club_pk>/leave/', LeaveClubView.as_view(), name='club_leave'),
    path('<int:club_pk>/remove-member/<int:member_pk>/', RemoveMemberView.as_view(), name='remove_member'),
    
    # URLs de Eventos
    path('<int:club_pk>/eventos/', EventListView.as_view(), name='event_list'),
    path('evento/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('<int:club_pk>/evento/agregar/', EventCreateView.as_view(), name='event_add'),
    path('evento/<int:pk>/editar/', EventUpdateView.as_view(), name='event_edit'),
    path('evento/<int:pk>/eliminar/', EventDeleteView.as_view(), name='event_delete'),
    path('evento/<int:event_pk>/comentar/', AddCommentView.as_view(), name='add_comment'),
    path('comentario/<int:comment_pk>/eliminar/', DeleteCommentView.as_view(), name='delete_comment'),
]

