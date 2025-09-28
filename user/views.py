from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from user.models import UserProfile
from user.serializers import UserProfileSerializer
from user.models import Friend
from django.contrib.auth.models import User
from rest_framework.response import Response


class AddFriendView(APIView):
    def post(self, request, user_id):
        from_user = request.user
        to_user = get_object_or_404(User, id=user_id)

        if Friend.objects.filter(from_user=from_user, to_user=to_user).exists():
            return Response({"message": "Already added."}, status=status.HTTP_200_OK)

        Friend.objects.create(from_user=from_user, to_user=to_user)

        sender_profile = UserProfile.objects.get(user_id=from_user.id)
        sender_profile.coins -= 50
        sender_profile.save()

        return Response({"message": "Friend added."}, status=status.HTTP_201_CREATED)
