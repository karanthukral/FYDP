from nara_backend.models import Traffic
from rest_framework import serializers

class TrafficSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Traffic
        fields = ('human_identifier', 'flagged', 'created_date', 'metadata')
