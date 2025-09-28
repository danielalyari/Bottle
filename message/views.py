from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from message.models import Message, Notif
from user.models import UserProfile, Friend
from message.serializers import MessageSerializer
from rest_framework import permissions


class SendMessageView(CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        saved_message = serializer.save()
        sender_profile = UserProfile.objects.get(user=saved_message.sender)
        sender_profile.coins -= 10
        sender_profile.save()

        followers = Friend.objects.filter(
            to_user=saved_message.sender).select_related('from_user')

        notifications = [
            Notif(reciver=friend.from_user, message=saved_message)
            for friend in followers
        ]
        Notif.objects.bulk_create(notifications)


class ReceiveMessageView(RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        message = self.get_object()
        receiver_id = message.receiver
        sender_profile = UserProfile.objects.get(user_id=receiver_id)
        sender_profile.coins -= 30
        sender_profile.save()

        serializer = self.get_serializer(message)
        return Response(serializer.data)


class ReplyToMessage(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        message = get_object_or_404(Message, pk=kwargs['pk'])

        reply_content = request.data.get("content")
        reply_message = Message.objects.create(
            sender=request.user,
            receiver=message.sender,
            content=reply_content,
            reply_to=message
        )

        sender_profile = UserProfile.objects.get(user=request.user)
        sender_profile.coins -= 20
        sender_profile.save()

        return Response(
            {"status": "success", "message": "Reply sent successfully."},
            status=status.HTTP_201_CREATED
        )


class ListMessagesView(ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAdminUser]


class ModelDeleteView(DestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAdminUser]


class AddCoinsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        user_profile = get_object_or_404(UserProfile, user_id=request.data.get("user_id"))

        coins_to_add = request.data.get("coins", 0)
        user_profile.coins += coins_to_add
        user_profile.save()
        return Response({"status": "success", "message": "Coins added successfully."})


class BanUserView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        user_profile = get_object_or_404(UserProfile, user_id=request.data.get("user_id"))

        user_profile.is_banned = True
        user_profile.save()
        return Response({"status": "success", "message": "User banned successfully."})