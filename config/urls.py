from django.urls import path

from desk import views


urlpatterns = [
    path("", views.list_tickets, name="ticket-list"),
    path("tickets/add/", views.add_ticket, name="ticket-add"),
    path("tickets/<int:pk>/status/", views.change_status, name="ticket-status"),
    path("tickets/<int:pk>/delete/", views.delete_ticket, name="ticket-delete"),
]
