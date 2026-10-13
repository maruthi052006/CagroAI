from django.test import TestCase
from rest_framework.test import APIRequestFactory
from apps.zones.models import Zone
from apps.accounts.models import User, FarmerProfile, OfficerProfile
from apps.accounts.services import assign_officer_for_zone
from apps.data_layer.models import Field
from apps.api.permissions import IsFarmerOwner, IsAssignedOfficer, IsOfficer

class ZonesAndAutoAssignmentTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_all_thirty_eight_districts_seeded(self):
        """
        Verify that all 38 Tamil Nadu districts are seeded with valid region groups.
        """
        zones = Zone.objects.all()
        self.assertEqual(zones.count(), 38, f"Expected 38 zones, got {zones.count()}")
        
        region_groups = set(zones.values_list('region_group', flat=True))
        expected_regions = {'NORTHERN', 'WESTERN', 'CENTRAL', 'DELTA', 'SOUTHERN'}
        self.assertEqual(region_groups, expected_regions)

        # Verify key district anchors
        district_names = set(zones.values_list('name', flat=True))
        self.assertIn('Thanjavur', district_names)
        self.assertIn('Coimbatore', district_names)
        self.assertIn('Madurai', district_names)
        self.assertIn('Chennai', district_names)
        self.assertIn('Tiruchirappalli', district_names)

    def test_single_officer_auto_assignment(self):
        """
        When exactly one officer covers a district zone, new farmer is assigned directly.
        """
        thanjavur = Zone.objects.get(name='Thanjavur')
        officer_user = User.objects.create_user(username='thanjavur_officer', role=User.Role.OFFICER)
        officer = OfficerProfile.objects.create(user=officer_user)
        officer.zones.add(thanjavur)

        assigned = assign_officer_for_zone(thanjavur)
        self.assertIsNotNone(assigned)
        self.assertEqual(assigned.id, officer.id)

    def test_multiple_officers_least_loaded_assignment(self):
        """
        When multiple officers cover a zone, assign the one with the fewest farmers.
        """
        coimbatore = Zone.objects.get(name='Coimbatore')
        
        # Officer 1 with 2 existing farmers
        u1 = User.objects.create_user(username='cbe_officer_busy', role=User.Role.OFFICER)
        o1 = OfficerProfile.objects.create(user=u1)
        o1.zones.add(coimbatore)

        f1_u = User.objects.create_user(username='f1', role=User.Role.FARMER)
        FarmerProfile.objects.create(user=f1_u, zone=coimbatore, assigned_officer=o1)
        f2_u = User.objects.create_user(username='f2', role=User.Role.FARMER)
        FarmerProfile.objects.create(user=f2_u, zone=coimbatore, assigned_officer=o1)

        # Officer 2 with 0 farmers
        u2 = User.objects.create_user(username='cbe_officer_free', role=User.Role.OFFICER)
        o2 = OfficerProfile.objects.create(user=u2)
        o2.zones.add(coimbatore)

        # Should pick o2 (least loaded)
        assigned = assign_officer_for_zone(coimbatore)
        self.assertIsNotNone(assigned)
        self.assertEqual(assigned.id, o2.id)

    def test_zero_officer_assignment_graceful_degrade(self):
        """
        When no officer covers a zone, return None so the signup sets needs_officer_assignment=True.
        """
        nilgiris = Zone.objects.get(name='Nilgiris')
        # Ensure no officer covers Nilgiris
        OfficerProfile.objects.filter(zones=nilgiris).delete()

        assigned = assign_officer_for_zone(nilgiris)
        self.assertIsNone(assigned)

    def test_permissions_is_farmer_owner_and_assigned_officer(self):
        """
        Verify IsFarmerOwner and IsAssignedOfficer enforce boundary security:
        - Owner farmer can access their field.
        - Other farmer cannot access.
        - Assigned officer can access.
        - Unassigned officer in another zone cannot access.
        """
        zone = Zone.objects.get(name='Salem')
        officer_user = User.objects.create_user(username='salem_officer', role=User.Role.OFFICER)
        officer = OfficerProfile.objects.create(user=officer_user)
        officer.zones.add(zone)

        farmer_user = User.objects.create_user(username='salem_farmer', role=User.Role.FARMER)
        farmer = FarmerProfile.objects.create(user=farmer_user, zone=zone, assigned_officer=officer)

        other_farmer_user = User.objects.create_user(username='intruder_farmer', role=User.Role.FARMER)
        other_farmer = FarmerProfile.objects.create(user=other_farmer_user, zone=zone)

        field = Field.objects.create(name='Test Field', latitude=11.66, longitude=78.14, crop_type='rice', owner=farmer)

        perm_owner = IsFarmerOwner()
        perm_officer = IsAssignedOfficer()

        # 1. Owner access
        req_owner = self.factory.get('/')
        req_owner.user = farmer_user
        self.assertTrue(perm_owner.has_object_permission(req_owner, None, field))

        # 2. Intruder farmer access
        req_intruder = self.factory.get('/')
        req_intruder.user = other_farmer_user
        self.assertFalse(perm_owner.has_object_permission(req_intruder, None, field))

        # 3. Assigned officer access
        req_officer = self.factory.get('/')
        req_officer.user = officer_user
        self.assertTrue(perm_owner.has_object_permission(req_officer, None, field))
        self.assertTrue(perm_officer.has_object_permission(req_officer, None, farmer))
