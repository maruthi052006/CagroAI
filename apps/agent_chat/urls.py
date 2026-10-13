from django.urls import path
from .views import PersonasListView, AgentChatMessageView, AgentChatHistoryView

urlpatterns = [
    path('personas/', PersonasListView.as_view(), name='agent-chat-personas'),
    path('<str:persona>/message/', AgentChatMessageView.as_view(), name='agent-chat-message'),
    path('<str:persona>/history/', AgentChatHistoryView.as_view(), name='agent-chat-history'),
]
