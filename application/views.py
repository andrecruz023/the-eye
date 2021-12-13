from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from application.models import Application
from application.serialzer import ApplicationSerializer


def get_error_response(status, error_details, message):
    return {
        "errorCode": status,  # 402, 400
        "errorDetails": error_details,  # // invalid_user
        "message": message  # // Email or passwordinvalid
    }


class ApplicationViewSet(mixins.ListModelMixin,
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
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def create(self, request, *args, **kwargs):
        params = dict(request.data)
        params['session_id'] = Application.genrate_session_id()
        serializer = ApplicationSerializer(data=params)
        if not serializer.is_valid():
            response_body = get_error_response(status.HTTP_400_BAD_REQUEST,
                                               'Invalid Request', 'Please provide valid information')
            return Response(response_body, status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.queryset.get(pk=kwargs.get('pk'))
        except Application.DoesNotExist:
            response_body = get_error_response(status.HTTP_400_BAD_REQUEST,
                                               'Not Found',
                                               'A Application with this id does not exist.')
            return Response(response_body, status.HTTP_400_BAD_REQUEST)
        application_serializer = self.serializer_class(instance, data=request.data, partial=True)
        application_serializer.is_valid(raise_exception=True)
        application_serializer.save()
        return Response(application_serializer.data, status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        application_serializer = Application.objects.all().order_by('timestamp')
        if not application_serializer:
            response_body = get_error_response(status.HTTP_400_BAD_REQUEST,
                                               'Not Found', 'No application added yet')
            return Response(response_body, status.HTTP_400_BAD_REQUEST)
        return Response(ApplicationSerializer(application_serializer, many=True).data, status.HTTP_200_OK)
