from django.urls import path
from .views import (
    ZoneListView, RegisterFarmerView, PredictView, 
    WhatIfView, ReassignZoneView, CropRegistryView,
    FieldListCreateView, HistoryView, SimulationStateView,
    SimulationTimelineView, DatasetInfoView, ModelRegistryView,
    DecisionRespondView, DecisionListView, OutcomeRecordView,
    OutcomeAccuracySummaryView, OfficerFarmersListView, OfficerFarmerDetailView,
    AuthMeView, AlertListCreateView, AlertMarkReadView,
    ConversationListCreateView, MessageListCreateView
)

urlpatterns = [
    path('zones/', ZoneListView.as_view(), name='zones'),
    path('auth/register/', RegisterFarmerView.as_view(), name='register'),
    path('auth/me/', AuthMeView.as_view(), name='auth-me'),
    path('fields/', FieldListCreateView.as_view(), name='fields'),
    path('predict/', PredictView.as_view(), name='predict'),
    path('history/', HistoryView.as_view(), name='history'),
    path('crop-registry/', CropRegistryView.as_view(), name='crop-registry'),
    path('simulate/what-if/', WhatIfView.as_view(), name='what-if'),
    path('simulation/<int:field_id>/state/', SimulationStateView.as_view(), name='simulation-state'),
    path('simulation/<int:field_id>/timeline/', SimulationTimelineView.as_view(), name='simulation-timeline'),
    path('dataset-info/', DatasetInfoView.as_view(), name='dataset-info'),
    path('model-registry/', ModelRegistryView.as_view(), name='model-registry'),
    
    # Decisions & Outcomes
    path('decisions/<int:prediction_id>/respond/', DecisionRespondView.as_view(), name='decision-respond'),
    path('decisions/', DecisionListView.as_view(), name='decisions'),
    path('outcomes/<int:field_id>/record/', OutcomeRecordView.as_view(), name='outcome-record'),
    path('outcomes/accuracy-summary/', OutcomeAccuracySummaryView.as_view(), name='outcome-accuracy-summary'),

    # Officer Portal
    path('officer/farmers/', OfficerFarmersListView.as_view(), name='officer-farmers'),
    path('officer/farmers/<int:id>/', OfficerFarmerDetailView.as_view(), name='officer-farmer-detail'),
    path('officer/farmers/<int:farmer_id>/reassign-zone/', ReassignZoneView.as_view(), name='reassign-zone'),

    # Alerts & Messaging
    path('alerts/', AlertListCreateView.as_view(), name='alerts'),
    path('alerts/<int:alert_id>/read/', AlertMarkReadView.as_view(), name='alert-mark-read'),
    path('messaging/conversations/', ConversationListCreateView.as_view(), name='conversations'),
    path('messaging/conversations/<int:conversation_id>/messages/', MessageListCreateView.as_view(), name='conversation-messages'),
]

