from rest_framework.routers import DefaultRouter

from application.views import ApplicationViewSet

application_router = DefaultRouter()
application_router.register(r'application', ApplicationViewSet, 'application')