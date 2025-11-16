from django.db import models
from django.contrib.auth.models import User
import json

class Deck(models.Model):
    """Model for flashcard decks"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def card_count(self):
        return self.flashcards.count()


class Flashcard(models.Model):
    """Model for individual flashcards"""
    deck = models.ForeignKey(Deck, related_name='flashcards', on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    spaced_repetition = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"{self.deck.name} - {self.question[:50]}"


class StudySession(models.Model):
    """Track study sessions and progress"""
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    correct_count = models.IntegerField(default=0)
    total_attempts = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Session for {self.deck.name} - {self.started_at}"
    
    @property
    def accuracy(self):
        if self.total_attempts == 0:
            return 0
        return round((self.correct_count / self.total_attempts) * 100)


class DeckComment(models.Model):
    """Comments on flashcard decks"""
    deck = models.ForeignKey(Deck, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.deck.name}"


class DeckLike(models.Model):
    """Likes for flashcard decks"""
    deck = models.ForeignKey(Deck, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['deck', 'user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} likes {self.deck.name}"
