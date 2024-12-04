from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.views.generic import CreateView
from django.urls import reverse

from azure.core.credentials import AzureKeyCredential
from azure.maps.search import MapsSearchClient
from azure.core.exceptions import HttpResponseError
import requests


from geopy.distance import geodesic

from ..models import FieldOp, AidRequest, AidLocation
from .geocode_form import AidLocationForm

# from icecream import ic
from django.views.generic import DeleteView
from django.urls import reverse_lazy


class AidLocationCreateView(LoginRequiredMixin, CreateView):
    """
    A Django class-based view for saving azure maps geocoded location
    """
    model = AidRequest
    form_class = AidLocationForm
    template_name = 'aidrequests/aidrequest_geocode.html'

    def get_success_url(self):
        return reverse('aidrequest_detail',
                       kwargs={'field_op': self.field_op.slug,
                               'pk': self.aid_request.pk}
                       )

    def check_address_azure(self):
        """
        Validate an address using Azure Maps API.

        :param address: The address string to validate.
        :return: A dictionary containing the response from Azure Maps.
        """
        azure_maps_key = settings.AZURE_MAPS_KEY
        # ic(azure_maps_key)
        if not azure_maps_key:
            return {"error": "Azure Maps key is not configured."}

        endpoint = "https://atlas.microsoft.com/search/address/json"

        query_address = f"{self.aid_request.street_address}, {self.aid_request.city}"
        query_address += f", {self.aid_request.state}, {self.aid_request.zip_code}, {self.aid_request.country}"

        params = {
            "api-version": "1.0",
            "subscription-key": azure_maps_key,
            "query": query_address,
            "lat": self.geocode_latitude,
            "lon": self.geocode_longitude
        }

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors

            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def geocode_address_azure(self):
        """
        Validate an address using Azure Maps API.

        :param address: The address string to validate.
        :return: A dictionary containing the response from Azure Maps.
        """
        azure_maps_key = settings.AZURE_MAPS_KEY
        # ic(azure_maps_key)
        if not azure_maps_key:
            return {"error": "Azure Maps key is not configured."}

        endpoint = "https://atlas.microsoft.com/geocode"

        query_address = (
            f"{self.aid_request.street_address} "
            f"{self.aid_request.city} "
            f"{self.aid_request.state} "
            f"{self.aid_request.country}"
        )

        params = {
            "api-version": "2023-06-01",
            "query": query_address,
            "coordinates": str(self.field_op.longitude) + "," + str(self.field_op.latitude)
        }

        headers = {
            "Subscription-Key": azure_maps_key
        }

        try:
            response = requests.get(endpoint, params=params, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors

            return response.json(), query_address

        except requests.RequestException as e:
            return {"error": str(e)}

    def getAddressGeocode(self):
        map_cred = AzureKeyCredential(settings.AZURE_MAPS_KEY)
        maps_search_client = MapsSearchClient(credential=map_cred,)
        query_address = (
            f"{self.aid_request.street_address} "
            f"{self.aid_request.city} "
            f"{self.aid_request.state} "
            f"{self.aid_request.country}"
        )
        field_op_coords = [self.field_op.longitude, self.field_op.latitude]
        results = {"status": None}
        try:
            query_results = maps_search_client.get_geocoding(query=query_address, coordinates=field_op_coords)

            if query_results.get('features', False):
                results['status'] = "Success"
                coordinates = query_results['features'][0]['geometry']['coordinates']
                results['latitude'] = round(coordinates[1], 5)
                results['longitude'] = round(coordinates[0], 5)
                results['features'] = query_results['features']

                results['confidence'] = query_results['features'][0]['properties']['confidence']
                results['found_address'] = query_results['features'][0]['properties']['address']['formattedAddress']
                results['locality'] = query_results['features'][0]['properties']['address']['locality']
                # results['neighborhood'] = query_results['features'][0]['properties']['address']['neighborhood']
                results['match_codes'] = query_results['features'][0]['properties']['matchCodes']
                results['match_type'] = query_results['features'][0]['properties']['type']
                return results
            else:
                results['status'] = "No Matches"
                return results

        except HttpResponseError as exception:
            if exception.error is not None:
                return exception.error.code, exception.error.message
            results['status'] = "HttpError"
            results['error_code'] = exception.error.code
            results['error_message'] = exception.error.message
            return results

    def setup(self, request, *args, **kwargs):
        """Initialize attributes shared by all view methods."""
        if hasattr(self, "get") and not hasattr(self, "head"):
            self.head = self.get
        self.request = request
        self.args = args
        self.kwargs = kwargs
        # custom setup
        self.field_op = get_object_or_404(FieldOp, slug=kwargs['field_op'])
        self.aid_request = get_object_or_404(AidRequest, pk=kwargs['pk'])
        self.geocode_results = self.getAddressGeocode()
        self.geocode_distance = round(geodesic(
            (self.geocode_results['latitude'], self.geocode_results['longitude']),
            (self.field_op.latitude, self.field_op.longitude)
            ).km, 1)
        self.geocode_latitude = self.geocode_results['latitude']
        self.geocode_longitude = self.geocode_results['longitude']
        self.geocode_confidence = self.geocode_results['confidence']
        self.geocode_source = 'azure_maps'

    def get_context_data(self, **kwargs):
        """ Add Action and Field_Op """
        context = super().get_context_data(**kwargs)
        action = self.request.GET.get('action') or None
        context['field_op'] = self.field_op
        context['aid_request'] = self.aid_request
        context['action'] = action
        context['distance'] = self.geocode_distance

        context['latitude'] = self.geocode_results['latitude']
        context['longitude'] = self.geocode_results['longitude']
        context['confidence'] = self.geocode_results['confidence']
        context['found_address'] = self.geocode_results['found_address']

        if action == 'search':
            action_results = self.check_address_azure()
            context['action_summary'] = action_results['summary']
            results = sorted(action_results['results'], key=lambda x: x['score'], reverse=True)
            context['results'] = results

        elif action == 'geocode':
            action_results, query_address = self.geocode_address_azure()
            context["query_address"] = query_address
            features = action_results['features']
            for feature in features:
                lat1 = feature['geometry']['coordinates'][1]
                lon1 = feature['geometry']['coordinates'][0]
                lat2 = self.field_op.latitude
                lon2 = self.field_op.longitude
                feature['distance'] = geodesic((lat1, lon1), (lat2, lon2)).km
            context['features'] = features
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        note = (
            f"{self.geocode_results['found_address']}\n"
            f"Distance: {self.geocode_distance} km\n"
            f"Confidence: {self.geocode_confidence}\n"
            f"Match Type: {self.geocode_results['match_type']}\n"
            f"Match Codes: {self.geocode_results['match_codes']}\n"
        )

        kwargs['initial'] = {
                'aid_request': self.aid_request.pk,
                'field_op': self.field_op.slug,
                'latitude': self.geocode_latitude,
                'longitude': self.geocode_longitude,
                'status': 'confirmed',
                'source': 'azure_maps',
                'note': note,
            }
        # ic(kwargs)
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        self.object.aid_request = self.aid_request
        user = self.request.user
        if user.is_authenticated:
            form.instance.created_by = user
            form.instance.updated_by = user
        else:
            form.instance.created_by = None
            form.instance.updated_by = None
        self.object.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class AidLocationDeleteView(LoginRequiredMixin, DeleteView):
    model = AidLocation
    template_name = 'aidrequests/aid_location_confirm_delete.html'
    context_object_name = 'aid_location'

    def get_success_url(self):
        return reverse_lazy(
            'aidrequest_detail',
            kwargs={
                'field_op': self.field_op.slug,
                'pk': self.aid_request.pk
                }
            )

    def setup(self, request, *args, **kwargs):
        """Initialize attributes shared by all view methods."""
        if hasattr(self, "get") and not hasattr(self, "head"):
            self.head = self.get
        self.request = request
        self.args = args
        self.kwargs = kwargs
        # self.aid_location = get_object_or_404(AidLocation, pk=kwargs['pk'])
        self.aid_request = get_object_or_404(AidRequest, pk=kwargs['aid_request'])
        self.field_op = self.aid_request.field_op

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['field_op'] = self.field_op
        context['aid_request'] = self.aid_request
        # ic(context)
        return context
