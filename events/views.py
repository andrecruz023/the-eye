from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from application.models import Application
from events.models import Events
from events.serializer import EventsSerializer, EventsDetailSerializer


def get_error_response(status, error_details, message):
    return {
        "errorCode": status,  # 402, 400
        "errorDetails": error_details,  # // invalid_user
        "message": message  # // Email or passwordinvalid
    }


class EventsViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    GenericViewSet):
    """
    The following endpoints are fully provided by mixins:
    * List view
    * Create view
    """
    queryset = Events.objects.all()
    serializer_class = EventsSerializer

    def create(self, request, *args, **kwargs):
        serializer = EventsSerializer(data=request.data)
        if not serializer.is_valid():
            response_body = get_error_response(status.HTTP_400_BAD_REQUEST,
                                               'Invalid Request', 'Please provide valid information')
            return Response(response_body, status.HTTP_400_BAD_REQUEST)
        else:
            events_serializer = serializer.save()
            return Response(events_serializer.data, status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.queryset.get(pk=kwargs.get('pk'))
        except Application.DoesNotExist:
            response_body = get_error_response(status.HTTP_400_BAD_REQUEST,
                                               'Not Found',
                                               'A events with this id does not exist.')
            return Response(response_body, status.HTTP_400_BAD_REQUEST)
        events_serializer = self.serializer_class(instance, data=request.data, partial=True)
        events_serializer.is_valid(raise_exception=True)
        events_serializer.save()
        return Response(events_serializer.data, status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        events_serializer = Events.objects.all().order_by('timestamp')
        if not events_serializer:
            response_body = get_error_response(status.HTTP_400_BAD_REQUEST,
                                               'Not Found', 'No events added yet')
            return Response(response_body, status.HTTP_400_BAD_REQUEST)
        return Response(EventsDetailSerializer(events_serializer, many=True).data, status.HTTP_200_OK)
