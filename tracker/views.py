from django.urls import reverse_lazy

from tracker.forms import TRACKER_FIELDS, TrackerForm
from tracker.models import Tracker
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class TrackerCreateView(LoginRequiredMixin, CreateView):
    model = Tracker
    form_class = TrackerForm
    template_name = "tracker_form.html"
    success_url = reverse_lazy("tracker-list")  # change as needed

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["dynamic_fields"] = TRACKER_FIELDS
        return kwargs

    def form_valid(self, form):
        form.save(user=self.request.user)
        return super().form_valid(form)
    
class TrackerUpdateView(LoginRequiredMixin, UpdateView):
    model = Tracker
    form_class = TrackerForm
    template_name = "tracker_form.html"
    success_url = reverse_lazy("tracker-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["dynamic_fields"] = TRACKER_FIELDS
        return kwargs

    def form_valid(self, form):
        form.save(user=self.request.user)
        return super().form_valid(form)
    
class TrackerListView(LoginRequiredMixin, ListView):
    model = Tracker
    template_name = "tracker_list.html"
    context_object_name = "trackers"

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get("status")
        q = self.request.GET.get("q")

        if status:
            queryset = queryset.filter(status=status)
        
        if q:
            from django.db.models import Q
            queryset = queryset.filter(
                Q(data__title__icontains=q) | 
                Q(data__description__icontains=q) |
                Q(ticket_id__icontains=q)
            )
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_trackers = Tracker.objects.all()
        
        # Calculate status counts
        status_counts = {
            "total": all_trackers.count(),
            "pending": all_trackers.filter(status=Tracker.Status.PENDING).count(),
            "approved": all_trackers.filter(status=Tracker.Status.APPROVED).count(),
            "rejected": all_trackers.filter(status=Tracker.Status.REJECTED).count(),
            "in_progress": all_trackers.filter(status=Tracker.Status.IN_PROGRESS).count(),
        }
        context["status_counts"] = status_counts

        # Calculate Total Value (Estimate)
        total_value: float = 0.0
        for t in all_trackers:
            amount_val = 0.0
            try:
                # Ensure data is a dict before calling .get()
                data = t.data if isinstance(t.data, dict) else {}
                amount_val = float(data.get("amount", 0))
            except (ValueError, TypeError, AttributeError):
                amount_val = 0.0
            
            # Move addition outside try block to help type inference
            total_value = total_value + amount_val
        context["total_value"] = total_value

        # Prepare Chart Data (Last 10 tickets with amounts)
        recent_tickets = all_trackers.order_by("-created_on")[:10][::-1] # 10 most recent, chronological
        chart_labels = []
        chart_amounts = []
        
        for t in recent_tickets:
            label = t.created_on.strftime("%b %d")
            amount = 0.0
            try:
                data = t.data if isinstance(t.data, dict) else {}
                amount_val = data.get("amount", 0)
                amount = float(amount_val)
            except (ValueError, TypeError, AttributeError):
                pass
            chart_labels.append(label)
            chart_amounts.append(amount)
        
        context["chart_labels"] = chart_labels
        context["chart_amounts"] = chart_amounts

        # Prepare extra stats for status distribution
        context["status_values"] = [
            status_counts["pending"],
            status_counts["in_progress"],
            status_counts["approved"],
            status_counts["rejected"],
        ]

        context["current_status"] = self.request.GET.get("status", "")
        context["search_query"] = self.request.GET.get("q", "")
        return context