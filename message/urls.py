from django.urls import path
from message.views import (SendMessageView, ReceiveRandomMessageView,
                           ReplyToMessage, AddCoinsView, BanUserView,
                           RevealSenderView, MessageDeleteView, ListMessagesView)


urlpatterns = [
    path('send/', SendMessageView.as_view(), name='send_message'),
    path("receive-random-message/", ReceiveRandomMessageView.as_view(), name="receive-random-message"),
    path("reveal-sender/<int:pk>/", RevealSenderView.as_view(), name="reveal-sender"),
    path('reply/<int:pk>/', ReplyToMessage.as_view(), name='reply_to_message'),
    path('add-coins/', AddCoinsView.as_view(), name='add_coins'),
    path('ban-user/', BanUserView.as_view(), name='ban_user'),
    path('list-messages/', ListMessagesView.as_view(), name='list_messages'),
    path('delete-message/<int:pk>/', MessageDeleteView.as_view(), name='delete_message'),
]