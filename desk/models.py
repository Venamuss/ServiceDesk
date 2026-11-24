from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models


class Ticket(models.Model):
    class Priority(models.TextChoices):
        LOW = "low", "Низкий"
        MEDIUM = "medium", "Средний"
        HIGH = "high", "Высокий"

    class Status(models.TextChoices):
        NEW = "new", "Новая"
        ACTIVE = "active", "В работе"
        CLOSED = "closed", "Закрыта"

    title = models.CharField("Тема", max_length=160, validators=[MinLengthValidator(5)])
    description = models.TextField("Описание", validators=[MinLengthValidator(10)])
    priority = models.CharField(
        "Приоритет", max_length=6, choices=Priority.choices, default=Priority.MEDIUM,
    )
    status = models.CharField(
        "Статус", max_length=6, choices=Status.choices, default=Status.NEW,
    )

    @property
    def next_status(self):
        return {
            self.Status.NEW: self.Status.ACTIVE,
            self.Status.ACTIVE: self.Status.CLOSED,
        }.get(self.status)

    def transition_to(self, target):
        if self.next_status is None or target != self.next_status:
            raise ValidationError("Этот переход статуса недоступен.")
        updated = Ticket.objects.filter(pk=self.pk, status=self.status).update(status=target)
        if not updated:
            raise ValidationError("Заявка уже изменилась. Проверьте её в списке.")
        self.status = target
