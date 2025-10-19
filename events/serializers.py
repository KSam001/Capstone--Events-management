from rest_framework import serializers
from .models import Event, RSVP

class EventSerializer(serializers.ModelSerializer):
    # Added host_email for easy display in the frontend
    host_email = serializers.ReadOnlyField(source='host.email')
    
    class Meta:
        model = Event
        fields = ['id', 'host', 'host_email', 'title', 'description', 'date', 'time', 'location', 'created_at']
        read_only_fields = ['host']

class RSVPReadSerializer(serializers.ModelSerializer):
    # Displays the attendee's email instead of just the ID
    attendee_email = serializers.ReadOnlyField(source='attendee.email')
    
    class Meta:
        model = RSVP
        fields = ['id', 'event', 'attendee', 'attendee_email', 'rsvped_at']
        
class RSVPWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RSVP
        fields = ['event', 'attendee']
        # Do not allow duplicates based on the unique_together constraint in the model
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=RSVP.objects.all(),
                fields=['event', 'attendee'],
                message="You have already RSVP'd to this event."
            )
        ]
