from django.contrib import admin
from .models import Deck, Flashcard, StudySession, DeckComment, DeckLike


@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ['name', 'card_count', 'is_public', 'owner', 'likes_count', 'created_at']
    list_filter = ['is_public', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    def likes_count(self, obj):
        return obj.likes.count()
    likes_count.short_description = 'Likes'


@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ['deck', 'question_preview', 'spaced_repetition', 'order', 'created_at']
    list_filter = ['spaced_repetition', 'deck', 'created_at']
    search_fields = ['question', 'answer']
    readonly_fields = ['created_at', 'updated_at']
    
    def question_preview(self, obj):
        return obj.question[:50] + '...' if len(obj.question) > 50 else obj.question
    question_preview.short_description = 'Question'


@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ['deck', 'user', 'accuracy', 'total_attempts', 'started_at', 'completed_at']
    list_filter = ['deck', 'started_at', 'completed_at']
    readonly_fields = ['started_at', 'accuracy']


@admin.register(DeckComment)
class DeckCommentAdmin(admin.ModelAdmin):
    list_display = ['deck', 'user', 'text_preview', 'created_at']
    list_filter = ['created_at', 'deck']
    search_fields = ['text', 'user__username', 'deck__name']
    readonly_fields = ['created_at']
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Comment'


@admin.register(DeckLike)
class DeckLikeAdmin(admin.ModelAdmin):
    list_display = ['deck', 'user', 'created_at']
    list_filter = ['created_at', 'deck']
    search_fields = ['user__username', 'deck__name']
    readonly_fields = ['created_at']
