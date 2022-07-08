from django.urls import path
from .views import BotMenuView

urlpatterns = [
    path('', BotMenuView.as_view(), name="bot")
]