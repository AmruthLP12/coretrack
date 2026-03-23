from django.db import models
from django.db import transaction
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder


def get_financial_year(d=None):
    d = d or timezone.now().date()

    if d.month >= 4:
        return f"{d.year}-{str(d.year + 1)[-2:]}"
    return f"{d.year - 1}-{str(d.year)[-2:]}"


# Create your models here.


class Tracker(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        IN_PROGRESS = "in_progress", "In Progress"
        RECOMMENDED = "recommended", "Recommended"
        DECLINED = "declined", "Declined"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        CANCELLED = "cancelled", "Cancelled"

    ticket_id = models.CharField(
        max_length=100, unique=True, editable=False, null=True, blank=True
    )

    requested_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="requested_tickets",
    )

    data = models.JSONField(default=dict, blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    updated_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="updated_tickets",
    )

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.ticket_id or "No Ticket ID"

    def generate_ticket_id(self):
        fy = get_financial_year()
        prefix = f"COM/{fy}/"

        with transaction.atomic():
            last_obj = (
                Tracker.objects.select_for_update()
                .filter(ticket_id__startswith=prefix)
                .order_by("-created_on")
                .first()
            )

            if last_obj and last_obj.ticket_id:
                try:
                    last_seq = int(last_obj.ticket_id.split("/")[-1])
                except (ValueError, AttributeError):
                    last_seq = 0
            else:
                last_seq = 0

            next_seq = str(last_seq + 1).zfill(4)
            return f"{prefix}{next_seq}"

    def save(self, *args, **kwargs):
        if not self.ticket_id:
            self.ticket_id = self.generate_ticket_id()
        super().save(*args, **kwargs)
