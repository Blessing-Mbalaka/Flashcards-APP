from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count
from django.contrib.auth.models import User
from .models import Deck, Flashcard, StudySession, DeckComment, DeckLike
from .serializers import (
    DeckSerializer, DeckListSerializer, FlashcardSerializer, 
    StudySessionSerializer, BulkUploadSerializer, UserRegisterSerializer,
    UserProfileSerializer, CommentSerializer, CommunityDeckSerializer
)


def index(request):
    """Serve the main flashcards page"""
    return render(request, 'flashcards/index.html')


class DeckViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Deck CRUD operations
    """
    queryset = Deck.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DeckListSerializer
        return DeckSerializer
    
    @action(detail=False, methods=['post'], parser_classes=[JSONParser, MultiPartParser, FormParser])
    def upload(self, request):
        """
        Upload flashcards from JSON file or data
        POST /api/decks/upload/
        """
        serializer = BulkUploadSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            # Create deck
            deck = Deck.objects.create(
                name=data['deck_name'],
                description=data.get('description', ''),
                is_public=data.get('is_public', False),
                owner=request.user if request.user.is_authenticated else None
            )
            
            # Create flashcards
            flashcards = []
            for idx, card_data in enumerate(data['flashcards']):
                flashcard = Flashcard(
                    deck=deck,
                    question=card_data['question'],
                    answer=card_data['answer'],
                    spaced_repetition=card_data.get('spacedRepetition', False),
                    order=idx
                )
                flashcards.append(flashcard)
            
            Flashcard.objects.bulk_create(flashcards)
            
            # Return created deck with flashcards
            deck_serializer = DeckSerializer(deck)
            return Response(deck_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def export(self, request, pk=None):
        """
        Export deck as JSON
        GET /api/decks/{id}/export/
        """
        deck = self.get_object()
        flashcards_data = [
            {
                'question': card.question,
                'answer': card.answer,
                'spacedRepetition': card.spaced_repetition
            }
            for card in deck.flashcards.all()
        ]
        
        return Response({
            'deck_name': deck.name,
            'description': deck.description,
            'flashcards': flashcards_data
        })
    
    @action(detail=False, methods=['get'])
    def public(self, request):
        """
        Get all public decks
        GET /api/decks/public/
        """
        public_decks = Deck.objects.filter(is_public=True)
        serializer = DeckListSerializer(public_decks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def community(self, request):
        """
        Get community/trending decks sorted by popularity
        GET /api/decks/community/
        """
        public_decks = Deck.objects.filter(is_public=True).annotate(
            likes_count=Count('likes')
        ).order_by('-likes_count', '-created_at')[:20]
        
        serializer = CommunityDeckSerializer(
            public_decks, 
            many=True, 
            context={'request': request}
        )
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        """
        Like a deck
        POST /api/decks/{id}/like/
        """
        deck = self.get_object()
        DeckLike.objects.get_or_create(deck=deck, user=request.user)
        return Response({
            'likes': deck.likes.count(),
            'message': 'Deck liked successfully'
        })
    
    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):
        """
        Unlike a deck
        DELETE /api/decks/{id}/unlike/
        """
        deck = self.get_object()
        DeckLike.objects.filter(deck=deck, user=request.user).delete()
        return Response({
            'likes': deck.likes.count(),
            'message': 'Like removed'
        })
    
    @action(detail=True, methods=['get', 'post'])
    def comments(self, request, pk=None):
        """
        Get or create comments for a deck
        GET /api/decks/{id}/comments/
        POST /api/decks/{id}/comments/
        """
        deck = self.get_object()
        
        if request.method == 'POST':
            if not request.user.is_authenticated:
                return Response(
                    {'error': 'Authentication required'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(deck=deck, user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # GET method
        comments = deck.comments.all()[:50]  # Limit to 50 most recent
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class FlashcardViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Flashcard CRUD operations
    """
    queryset = Flashcard.objects.all()
    serializer_class = FlashcardSerializer
    
    def get_queryset(self):
        queryset = Flashcard.objects.all()
        deck_id = self.request.query_params.get('deck', None)
        if deck_id:
            queryset = queryset.filter(deck_id=deck_id)
        return queryset


class StudySessionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Study Session tracking
    """
    queryset = StudySession.objects.all()
    serializer_class = StudySessionSerializer
    
    @action(detail=True, methods=['post'])
    def record_answer(self, request, pk=None):
        """
        Record answer as correct or incorrect
        POST /api/sessions/{id}/record_answer/
        Body: {"correct": true/false}
        """
        session = self.get_object()
        is_correct = request.data.get('correct', False)
        
        session.total_attempts += 1
        if is_correct:
            session.correct_count += 1
        session.save()
        
        serializer = self.get_serializer(session)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """
        Mark session as completed
        POST /api/sessions/{id}/complete/
        """
        from django.utils import timezone
        session = self.get_object()
        session.completed_at = timezone.now()
        session.save()
        
        serializer = self.get_serializer(session)
        return Response(serializer.data)


class RegisterView(generics.CreateAPIView):
    """User registration endpoint"""
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class UserProfileView(APIView):
    """Get current user profile with stats"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
