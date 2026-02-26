from rest_framework import serializers
from .models import ChatLog, ChatMessage, DocumentExport, CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']

class ChatMessageSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = ChatMessage
        fields = ['id', 'content', 'time', 'user_details']

class ChatLogSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = ChatLog
        fields = ['id', 'title', 'start_time', 'messages']

class DocumentExportSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentExport
        fields = ['id', 'status', 'file', 'created_at']
