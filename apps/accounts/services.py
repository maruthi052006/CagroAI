from apps.accounts.models import OfficerProfile
from django.db.models import Count
from apps.zones.models import Zone
from apps.alerts.models import Alert

def assign_officer_for_zone(zone: Zone) -> OfficerProfile | None:
    # Query all OfficerProfile records where zones includes this zone AND user.is_active=True
    officers = OfficerProfile.objects.filter(zones=zone, user__is_active=True).annotate(
        farmer_count=Count('assigned_farmers')
    ).order_by('farmer_count')
    
    if officers.exists():
        # Returns the officer with fewest farmers (first after order_by)
        return officers.first()
    
    # If NO officer currently covers that zone, logic in view will set needs_officer_assignment=True
    # and create an alert for the admin
    return None
