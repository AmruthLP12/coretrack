from django.urls import reverse_lazy

from tracker.forms import TRACKER_FIELDS, TrackerForm
from tracker.models import Tracker
from django.views.generic import CreateView, UpdateView,ListView
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
    
class TrackerUpdateView(LoginRequiredMixin,UpdateView):
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
    
class TrackerListView(LoginRequiredMixin,ListView):
    model = Tracker
    template_name = "tracker_list.html"
    context_object_name = "trackers"