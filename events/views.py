from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Event, RSVP
from .serializers import EventSerializer, RSVPReadSerializer, RSVPWriteSerializer
from django.shortcuts import get_object_or_404

# Helper permission class (re-defined here to ensure it's in the file)
class IsHostOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow hosts of an event to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the host of the event
        return obj.host == request.user

class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Events. 
    Allows authenticated users to create, update, delete their own events.
    Allows all users (authenticated or not) to view events.
    """
    queryset = Event.objects.all().order_by('date', 'time')
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """Sets the host field to the current user upon event creation."""
        serializer.save(host=self.request.user)

    def get_permissions(self):
        """Allows hosts to edit/delete their own events."""
        if self.action in ['update', 'partial_update', 'destroy']:
            # The IsHostOrReadOnly permission needs to be used here
            return [permissions.IsAuthenticated(), IsHostOrReadOnly()]
        return super().get_permissions()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def rsvp(self, request, pk=None):
        """
        Custom action to allow a user to RSVP to an event or cancel an existing RSVP.
        """
        event = get_object_or_404(Event, pk=pk)
        user = request.user
        
        # Check if RSVP already exists
        rsvp_obj = RSVP.objects.filter(event=event, attendee=user).first()

        if rsvp_obj:
            # If RSVP exists, delete it (cancel RSVP)
            rsvp_obj.delete()
            return Response({'status': 'RSVP cancelled'}, status=204) # 204 No Content

        else:
            # If RSVP does not exist, create a new one
            serializer = RSVPWriteSerializer(data={'event': event.id, 'attendee': user.id})
            serializer.is_valid(raise_exception=True)
            serializer.save(event=event, attendee=user)
            return Response({'status': 'RSVP successful'}, status=201) # 201 Created
        
    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def attendees(self, request, pk=None):
        """
        Custom action to retrieve the list of attendees for a specific event.
        """
        event = get_object_or_404(Event, pk=pk)
        attendees = RSVP.objects.filter(event=event)
        
        # Use the Read Serializer to display attendee details
        serializer = RSVPReadSerializer(attendees, many=True)
        return Response(serializer.data)
