from rest_framework import serializers

from application.serialzer import ApplicationSerializer
from events.models import Events


class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = "__all__"


class EventsDetailSerializer(serializers.ModelSerializer):
    session_id = serializers.SerializerMethodField('get_session_id', read_only=True)
    name = serializers.SerializerMethodField('get_name', read_only=True)
    category = serializers.SerializerMethodField('get_category', read_only=True)

    def get_session_id(self, obj):
        return obj.application.session_id

    def get_name(self, obj):
        return obj.application.name

    def get_category(self, obj):
        return obj.application.category

    class Meta:
        model = Events
        fields = ('session_id', 'name', 'category', "data", 'timestamp')
