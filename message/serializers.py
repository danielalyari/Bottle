from rest_framework import serializers
from message.models import Message
from user.serializers import BasicUserSerializer


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ('id', 'content', 'reply_to', 'sender', 'receiver')

    def get_sender(self, obj):
        if self.context.get('show_sender', False):
            return BasicUserSerializer(obj.sender).data
        return None