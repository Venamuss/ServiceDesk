from django import forms

from .models import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "priority"]
        widgets = {"description": forms.Textarea(attrs={"rows": 5})}
        help_texts = {
            "title": "От 5 до 160 символов.",
            "description": "Не менее 10 символов.",
        }
