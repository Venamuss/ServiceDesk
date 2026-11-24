from django.core.exceptions import ValidationError
from django.test import SimpleTestCase, TestCase

from .forms import TicketForm
from .models import Ticket


class TicketValidationTests(SimpleTestCase):
    def form(self, title="Почта", description="0123456789", priority="medium"):
        return TicketForm({
            "title": title,
            "description": description,
            "priority": priority,
        })

    def test_title_with_four_characters_is_rejected_after_trimming(self):
        self.assertEqual(self.form(title="  Сеть  ").errors.as_data()["title"][0].code, "min_length")

    def test_title_with_five_characters_is_accepted(self):
        form = self.form(title="  Почта  ")
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["title"], "Почта")

    def test_description_with_nine_characters_is_rejected(self):
        self.assertEqual(
            self.form(description="012345678").errors.as_data()["description"][0].code,
            "min_length",
        )

    def test_description_with_ten_characters_is_accepted(self):
        form = self.form(description="0123456789")
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["description"], "0123456789")

    def test_unknown_priority_is_rejected(self):
        self.assertEqual(
            self.form(priority="urgent").errors.as_data()["priority"][0].code,
            "invalid_choice",
        )


class TicketTransitionTests(TestCase):
    def setUp(self):
        self.ticket = Ticket.objects.create(title="Почта", description="Не открывается почта")

    def test_new_ticket_moves_to_active(self):
        self.assertEqual(self.ticket.status, Ticket.Status.NEW)
        self.ticket.transition_to(Ticket.Status.ACTIVE)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, Ticket.Status.ACTIVE)

    def test_active_ticket_moves_to_closed(self):
        self.ticket.transition_to(Ticket.Status.ACTIVE)
        self.ticket.transition_to(Ticket.Status.CLOSED)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, Ticket.Status.CLOSED)

    def test_new_ticket_cannot_skip_active(self):
        with self.assertRaises(ValidationError):
            self.ticket.transition_to(Ticket.Status.CLOSED)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, Ticket.Status.NEW)

    def test_closed_ticket_cannot_reopen(self):
        self.ticket.transition_to(Ticket.Status.ACTIVE)
        self.ticket.transition_to(Ticket.Status.CLOSED)
        with self.assertRaises(ValidationError):
            self.ticket.transition_to(Ticket.Status.ACTIVE)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, Ticket.Status.CLOSED)

    def test_stale_state_cannot_overwrite_current_status(self):
        stale_ticket = Ticket.objects.get(pk=self.ticket.pk)
        self.ticket.transition_to(Ticket.Status.ACTIVE)
        self.ticket.transition_to(Ticket.Status.CLOSED)
        with self.assertRaises(ValidationError):
            stale_ticket.transition_to(Ticket.Status.ACTIVE)
        stale_ticket.refresh_from_db()
        self.assertEqual(stale_ticket.status, Ticket.Status.CLOSED)
