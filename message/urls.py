from django.urls import path
from message.views import (SendMessageView, ReceiveMessageView,
                           ReplyToMessage, AddCoinsView, BanUserView)


urlpatterns = [
    path('send/', SendMessageView.as_view(), name='send_message'),
    path('receive/<int:pk>/', ReceiveMessageView.as_view(), name='receive_message'),
    path('reply/<int:pk>/', ReplyToMessage.as_view(), name='reply_to_message'),
    path('add-coins/', AddCoinsView.as_view(), name='add_coins'),
    path('ban-user/', BanUserView.as_view(), name='ban_user'),
]
