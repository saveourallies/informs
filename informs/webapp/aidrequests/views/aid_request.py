from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from django_q.tasks import async_chain

from geopy.distance import geodesic
from jinja2 import Template

from ..models import AidRequest, FieldOp, AidRequestLog
from ..tasks import aid_request_postsave
from takserver.cot import send_cots
from .aid_request_forms import AidRequestCreateForm, AidRequestUpdateForm, AidRequestLogForm

from icecream import ic


def has_location_status(aid_request, status):
    """
    Check if any of the aid_request locations have the matching status.

    :param aid_request: The AidRequest instance to check.
    :param status: location status you seek
    :return: found (boolean), and locations list
    """
    found = aid_request.locations.filter(status=status).exists()
    locations = aid_request.locations.filter(status=status)
    return found, locations


def geodist(aid_request):
    if any([aid_request.latitude, aid_request.longitude, aid_request.field_op.latitude,
            aid_request.field_op.longitude]) is None:
        return None

    return round(
        geodesic(
            (aid_request.latitude, aid_request.longitude),
            (aid_request.field_op.latitude, aid_request.field_op.longitude)
            ).km, 1)


def format_aid_location_note(aid_location):
    """
    Format a text string using Jinja2 and aid_location data.

    :param aid_location: The AidLocation instance to format.
    :return: Formatted text string.
    """
    if aid_location.source == "azure_maps":
        template_str = "Geocode Note:\n{{ aid_location.note }}"
    elif aid_location.source == "manual":
        template_str = """
        Aid Location Details:
        ---------------------
        ID: {{ aid_location.pk }}
        Source: {{ aid_location.source }}
        Created: {{ aid_location.created_at.strftime('%Y-%m-%d %H:%M') }}
        By: {{ aid_location.created_by }}
        """
        template_str = "\n".join([line.strip() for line in template_str.split('\n')])
    else:
        template_str = "Location Note:\n{{ aid_location.note }}"

    template = Template(template_str)
    return template.render(aid_location=aid_location)


# Create View for AidRequest
class AidRequestCreateView(CreateView):
    """ Aid Request - Create """
    model = AidRequest
    form_class = AidRequestCreateForm
    template_name = 'aidrequests/aid_request_form.html'
    # should return to Field Op Home
    success_url = reverse_lazy('home')

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.field_op = get_object_or_404(FieldOp, slug=kwargs['field_op'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['field_op'] = self.field_op
        if self.object is None:
            context['New'] = True
        else:
            context['New'] = False
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'field_op': self.field_op.pk}
        return kwargs

    def form_valid(self, form):
        self.object = form.save()

        if not self.object.requestor_email and not self.object.requestor_phone:
            form.add_error(None, 'Provide one of phone or email.')
            return self.form_invalid(form)
        user = self.request.user
        if user.is_authenticated:
            self.object.created_by = user
            self.object.updated_by = user
        else:
            self.object.created_by = None
            self.object.updated_by = None
        self.object.save()

        # ----- post save starts here ------
        updated_at_stamp = self.object.updated_at.strftime('%Y%m%d%H%M%S')
        # ic(self.object.__dict__.keys())
        savetype = 'new'
        postsave_tasks = async_chain([
            (aid_request_postsave, [self.object], {
                'savetype': savetype,
                'task_name': f"AR{self.object.pk}-AidRequestNew-Email-{updated_at_stamp}"}),
            (send_cots, [self.object], {
                'task_name': f"AR{self.object.pk}-AidRequestNew-TAK-{updated_at_stamp}"})
                ])
        ic('postsave_tasks', postsave_tasks)
        return super().form_valid(form)


# Update View for AidRequest
class AidRequestUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'aidrequests.change_aidrequest'
    model = AidRequest
    form_class = AidRequestUpdateForm
    template_name = 'aidrequests/aid_request_update.html'

    def get_success_url(self):
        return reverse_lazy('aid_request_list', kwargs={'field_op': self.kwargs['field_op']})

    def get_context_data(self, **kwargs):
        field_op_slug = self.kwargs['field_op']
        context = super().get_context_data(**kwargs)
        field_op = get_object_or_404(FieldOp, slug=field_op_slug)
        context['field_op'] = field_op
        return context

    def form_valid(self, form):
        self.object = form.save()
        field_op_slug = self.kwargs['field_op']
        field_op = FieldOp.objects.get(slug=field_op_slug)
        # this locks the field_op to the URL regardless of form values
        self.object.field_op = field_op
        # check either or email/phone
        if not self.object.requestor_email and not self.object.requestor_phone:
            form.add_error(None, 'Provide one of phone or email.')
            return self.form_invalid(form)
        user = self.request.user
        if user.is_authenticated:
            form.instance.updated_by = user
        else:
            form.instance.updated_by = None
        self.object.save()
        return super().form_valid(form)


class AidRequestLogCreateView(LoginRequiredMixin, CreateView):
    """ Aid Request Log - Create """
    model = AidRequestLog
    form_class = AidRequestLogForm

    def get_success_url(self):
        return reverse('aid_request_detail',
                       kwargs={
                           'field_op': self.field_op.slug,
                           'pk': self.aid_request.pk}
                       )

    def setup(self, request, *args, **kwargs):
        """Initialize attributes shared by all view methods."""
        super().setup(request, *args, **kwargs)
        # custom setup
        self.field_op = get_object_or_404(FieldOp, slug=kwargs['field_op'])
        self.aid_request = get_object_or_404(AidRequest, pk=kwargs['pk'])

    def form_valid(self, form):
        self.object = form.save()
        field_op_slug = self.kwargs['field_op']
        field_op = FieldOp.objects.get(slug=field_op_slug)
        self.object.field_op = field_op

        user = self.request.user
        if user.is_authenticated:
            self.object.created_by = user
            self.object.updated_by = user
        else:
            self.object.created_by = None
            self.object.updated_by = None
        self.object.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {
                'aid_request': self.aid_request.pk,
                'field_op': self.field_op.slug,
        }
        return kwargs
