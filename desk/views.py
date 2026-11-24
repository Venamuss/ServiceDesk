from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from .forms import TicketForm
from .models import Ticket


@require_GET
def list_tickets(request):
    status = request.GET.get("status", "")
    if status not in Ticket.Status.values:
        status = ""
    sort = "oldest" if request.GET.get("sort") == "oldest" else "newest"
    tickets = Ticket.objects.order_by("id" if sort == "oldest" else "-id")
    if status:
        tickets = tickets.filter(status=status)
    return render(request, "ticket_list.html", {
        "tickets": tickets,
        "status_choices": Ticket.Status.choices,
        "status": status,
        "sort": sort,
    })


@require_http_methods(["GET", "POST"])
def add_ticket(request):
    form = TicketForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        ticket = form.save()
        messages.success(request, f"Заявка №{ticket.pk} добавлена.")
        return redirect("ticket-list")
    return render(request, "ticket_form.html", {"form": form})


@require_POST
def change_status(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    try:
        ticket.transition_to(request.POST.get("status"))
    except ValidationError as error:
        messages.error(request, error.message)
    else:
        messages.success(request, f"Статус заявки №{pk}: {ticket.get_status_display()}.")
    return redirect("ticket-list")


@require_http_methods(["GET", "POST"])
def delete_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == "POST" and request.POST.get("confirm") == "yes":
        ticket.delete()
        messages.success(request, f"Заявка №{pk} удалена.")
        return redirect("ticket-list")
    return render(request, "ticket_delete.html", {"ticket": ticket})
