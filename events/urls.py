from rest_framework.routers import DefaultRouter

from events.views import EventsViewSet

events_router = DefaultRouter()
events_router.register(r'events', EventsViewSet, 'events')