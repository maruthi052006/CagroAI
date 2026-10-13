from rest_framework import serializers
from apps.data_layer.models import Field, FieldRecord, PredictionLog
from apps.accounts.models import FarmerProfile, OfficerProfile, User
from apps.zones.models import Zone
from apps.simulation.models import FieldSimulationState
from apps.api.models import MLModelVersion
from django.contrib.auth import get_user_model
from apps.accounts.services import assign_officer_for_zone

class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ['id', 'name', 'code', 'region_group']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        
class FarmerRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    zone_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = FarmerProfile
        fields = ['user', 'zone_id']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        zone_id = validated_data.pop('zone_id')
        user = User.objects.create_user(**user_data, role=User.Role.FARMER)
        zone = Zone.objects.get(id=zone_id)
        
        farmer = FarmerProfile.objects.create(user=user, zone=zone)
        officer = assign_officer_for_zone(zone)
        if officer:
            farmer.assigned_officer = officer
        else:
            farmer.needs_officer_assignment = True
        farmer.save()
        return farmer

class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = '__all__'

class PredictionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictionLog
        fields = ['id', 'field', 'timestamp', 'output_data']

class SimulationStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldSimulationState
        fields = '__all__'

class MLModelVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLModelVersion
        fields = ['id', 'agent_name', 'version', 'algorithm_description', 'metrics', 'trained_at', 'is_active']

class WhatIfRequestSerializer(serializers.Serializer):
    field_id = serializers.IntegerField()
    adjustments = serializers.JSONField()

from apps.coordination.models import DecisionRecord, OutcomeRecord
from apps.alerts.models import Alert
from apps.messaging.models import Conversation, Message

class DecisionRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DecisionRecord
        fields = '__all__'

class OutcomeRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutcomeRecord
        fields = '__all__'

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'sender_username', 'type', 'text_content', 'attachment', 'thumbnail', 'duration_seconds', 'status', 'sent_at']

class ConversationSerializer(serializers.ModelSerializer):
    farmer_name = serializers.CharField(source='farmer.user.username', read_only=True)
    officer_name = serializers.CharField(source='officer.user.username', read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'farmer', 'officer', 'farmer_name', 'officer_name', 'created_at', 'last_message']

    def get_last_message(self, obj):
        last = obj.messages.order_by('-sent_at').first()
        if last:
            return {'text': last.text_content, 'type': last.type, 'sent_at': last.sent_at}
        return None
