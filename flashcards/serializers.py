from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Deck, Flashcard, StudySession, DeckComment, DeckLike


class FlashcardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flashcard
        fields = ['id', 'question', 'answer', 'spaced_repetition', 'order', 'created_at']
        read_only_fields = ['id', 'created_at']


class DeckSerializer(serializers.ModelSerializer):
    flashcards = FlashcardSerializer(many=True, read_only=True)
    card_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Deck
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 
                  'is_public', 'card_count', 'flashcards']
        read_only_fields = ['id', 'created_at', 'updated_at', 'card_count']


class DeckListSerializer(serializers.ModelSerializer):
    """Lighter serializer for listing decks without all flashcards"""
    card_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Deck
        fields = ['id', 'name', 'description', 'created_at', 'card_count', 'is_public']


class StudySessionSerializer(serializers.ModelSerializer):
    accuracy = serializers.ReadOnlyField()
    deck_name = serializers.CharField(source='deck.name', read_only=True)
    
    class Meta:
        model = StudySession
        fields = ['id', 'deck', 'deck_name', 'started_at', 'completed_at', 
                  'correct_count', 'total_attempts', 'accuracy']
        read_only_fields = ['id', 'started_at', 'accuracy']


class BulkUploadSerializer(serializers.Serializer):
    """Serializer for bulk uploading flashcards from JSON"""
    deck_name = serializers.CharField(max_length=200)
    description = serializers.CharField(required=False, allow_blank=True)
    flashcards = serializers.ListField(
        child=serializers.DictField()
    )
    is_public = serializers.BooleanField(default=False)
    
    def validate_flashcards(self, value):
        """Validate flashcards structure"""
        for card in value:
            if 'question' not in card or 'answer' not in card:
                raise serializers.ValidationError(
                    "Each flashcard must have 'question' and 'answer' fields"
                )
        return value


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id']


class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords don't match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Detailed user profile with stats"""
    decks_created = serializers.SerializerMethodField()
    total_cards = serializers.SerializerMethodField()
    study_sessions = serializers.SerializerMethodField()
    total_correct = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'decks_created', 'total_cards', 
                  'study_sessions', 'total_correct']
    
    def get_decks_created(self, obj):
        return obj.deck_set.count()
    
    def get_total_cards(self, obj):
        return Flashcard.objects.filter(deck__owner=obj).count()
    
    def get_study_sessions(self, obj):
        return obj.studysession_set.count()
    
    def get_total_correct(self, obj):
        return sum(s.correct_count for s in obj.studysession_set.all())


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for deck comments"""
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = DeckComment
        fields = ['id', 'username', 'text', 'created_at']
        read_only_fields = ['id', 'username', 'created_at']


class CommunityDeckSerializer(serializers.ModelSerializer):
    """Serializer for community deck listing with social features"""
    card_count = serializers.ReadOnlyField()
    owner_name = serializers.CharField(source='owner.username', read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Deck
        fields = ['id', 'name', 'description', 'card_count', 'owner_name', 
                  'likes_count', 'comments_count', 'is_liked', 'created_at']
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False
