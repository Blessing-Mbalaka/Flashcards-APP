# FEATURE IMPLEMENTATION GUIDE

## 🔐 Authentication (30 minutes)

### Step 1: Install JWT
```bash
pip install djangorestframework-simplejwt
```

### Step 2: Update settings.py
```python
INSTALLED_APPS += ['rest_framework_simplejwt']

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
```

### Step 3: Add to urls.py
```python
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns += [
    path('api/login/', TokenObtainPairView.as_view()),
    path('api/register/', RegisterView.as_view()),
    path('api/profile/', UserProfileView.as_view()),
]
```

### Step 4: Frontend (add to index.html)
```javascript
// Login function
async function login(username, password) {
    const response = await fetch('/api/login/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username, password})
    });
    const data = await response.json();
    localStorage.setItem('access_token', data.access);
    localStorage.setItem('refresh_token', data.refresh);
}

// Add to all API calls
const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
};
```

---

## 👤 User Profile Header (15 minutes)

### Add to views.py
```python
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
            'decks_created': user.deck_set.count(),
            'total_cards': Flashcard.objects.filter(deck__owner=user).count(),
            'study_sessions': user.studysession_set.count(),
            'total_correct': sum(s.correct_count for s in user.studysession_set.all()),
        })
```

### Frontend - Add header component
```html
<div class="user-header" style="display: none;" id="userHeader">
    <img src="" id="userAvatar" class="avatar">
    <span id="userName"></span>
    <span id="userStats"></span>
    <button onclick="logout()">Logout</button>
</div>
```

```javascript
async function loadUserProfile() {
    const token = localStorage.getItem('access_token');
    if (!token) return;
    
    const response = await fetch('/api/profile/', {
        headers: {'Authorization': `Bearer ${token}`}
    });
    const user = await response.json();
    
    document.getElementById('userName').textContent = user.username;
    document.getElementById('userStats').textContent = 
        `${user.decks_created} decks • ${user.study_sessions} sessions`;
    document.getElementById('userHeader').style.display = 'flex';
}
```

---

## 🌐 Community Forum (45 minutes)

### Step 1: Add models (flashcards/models.py)
```python
class DeckComment(models.Model):
    deck = models.ForeignKey(Deck, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

class DeckLike(models.Model):
    deck = models.ForeignKey(Deck, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['deck', 'user']
```

### Step 2: Add serializers
```python
class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = DeckComment
        fields = ['id', 'username', 'text', 'created_at']

class CommunityDeckSerializer(serializers.ModelSerializer):
    card_count = serializers.ReadOnlyField()
    owner_name = serializers.CharField(source='owner.username', read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    class Meta:
        model = Deck
        fields = ['id', 'name', 'description', 'card_count', 'owner_name', 
                  'likes_count', 'comments_count', 'created_at']
```

### Step 3: Add endpoints to DeckViewSet
```python
@action(detail=True, methods=['post'])
def like(self, request, pk=None):
    deck = self.get_object()
    DeckLike.objects.get_or_create(deck=deck, user=request.user)
    return Response({'likes': deck.likes.count()})

@action(detail=True, methods=['delete'])
def unlike(self, request, pk=None):
    deck = self.get_object()
    DeckLike.objects.filter(deck=deck, user=request.user).delete()
    return Response({'likes': deck.likes.count()})

@action(detail=True, methods=['get', 'post'])
def comments(self, request, pk=None):
    deck = self.get_object()
    
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(deck=deck, user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    comments = deck.comments.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

@action(detail=False, methods=['get'])
def community(self, request):
    # Get trending/popular decks
    public_decks = Deck.objects.filter(is_public=True).annotate(
        likes_count=Count('likes')
    ).order_by('-likes_count', '-created_at')
    serializer = CommunityDeckSerializer(public_decks, many=True)
    return Response(serializer.data)
```

### Step 4: Frontend - Community Feed
```html
<div class="sidebar-card">
    <h3>🌐 Community Feed</h3>
    <div id="communityFeed"></div>
</div>
```

```javascript
async function loadCommunityFeed() {
    const response = await fetch('/api/decks/community/');
    const decks = await response.json();
    
    const html = decks.map(deck => `
        <div class="community-deck-item">
            <h4>${deck.name}</h4>
            <p>${deck.description}</p>
            <div class="deck-meta">
                <span>👤 ${deck.owner_name}</span>
                <span>❤️ ${deck.likes_count}</span>
                <span>💬 ${deck.comments_count}</span>
                <span>📚 ${deck.card_count} cards</span>
            </div>
            <button onclick="viewDeck(${deck.id})">Study</button>
            <button onclick="likeDeck(${deck.id})">Like</button>
        </div>
    `).join('');
    
    document.getElementById('communityFeed').innerHTML = html;
}

async function likeDeck(deckId) {
    const token = localStorage.getItem('access_token');
    await fetch(`/api/decks/${deckId}/like/`, {
        method: 'POST',
        headers: {'Authorization': `Bearer ${token}`}
    });
    loadCommunityFeed(); // Refresh
}
```

---

## 🎯 Complete Feature Summary

### What You'll Add:
1. **JWT Authentication** - Secure login/logout
2. **User Registration** - Sign up form
3. **Profile Header** - Show user info and stats
4. **Community Feed** - Browse public decks
5. **Like System** - Like/unlike decks
6. **Comments** - Discuss flashcard decks
7. **Trending Decks** - Sort by popularity

### API Endpoints to Add:
```
POST /api/login/
POST /api/register/
GET  /api/profile/
GET  /api/decks/community/
POST /api/decks/{id}/like/
DELETE /api/decks/{id}/unlike/
GET  /api/decks/{id}/comments/
POST /api/decks/{id}/comments/
```

### Database Changes:
```bash
# Add new models
python manage.py makemigrations
python manage.py migrate
```

---

## ⏱️ Time Estimates

- Authentication: **30 minutes**
- Profile Header: **15 minutes**
- Community Feed: **45 minutes**
- Polish & Testing: **30 minutes**

**Total: ~2 hours** for a full social learning platform! 🚀

---

## 💡 Why This Is Easy

✅ **Your architecture is perfect** for social features  
✅ **Already have User model** from Django  
✅ **API-first design** makes adding endpoints trivial  
✅ **Frontend is ready** - just add new fetch calls  
✅ **Database models** are simple to extend  
✅ **No template rewrites** needed  

You basically just:
1. Add 2-3 new models
2. Add 5-6 API endpoints
3. Add JavaScript functions to call them
4. Style the new UI components

**That's it!** 🎉
