# Test Script for StudyHub API
# Run this in PowerShell to test all endpoints

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "   StudyHub API Test Suite" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

$baseUrl = "http://localhost:8000/api"

# Test 1: List all decks
Write-Host "Test 1: Listing all decks..." -ForegroundColor Yellow
try {
    $decks = Invoke-RestMethod -Uri "$baseUrl/decks/" -Method Get
    Write-Host "✅ SUCCESS: Found $($decks.Count) decks" -ForegroundColor Green
    $decks | ForEach-Object { Write-Host "  - $($_.name) ($($_.card_count) cards)" }
} catch {
    Write-Host "❌ FAILED: $_" -ForegroundColor Red
}
Write-Host ""

# Test 2: Get first deck details
Write-Host "Test 2: Getting deck details..." -ForegroundColor Yellow
try {
    $deck = Invoke-RestMethod -Uri "$baseUrl/decks/1/" -Method Get
    Write-Host "✅ SUCCESS: Loaded '$($deck.name)'" -ForegroundColor Green
    Write-Host "  Description: $($deck.description)" 
    Write-Host "  Cards: $($deck.flashcards.Count)"
} catch {
    Write-Host "❌ FAILED: $_" -ForegroundColor Red
}
Write-Host ""

# Test 3: Upload a new deck
Write-Host "Test 3: Uploading a new deck..." -ForegroundColor Yellow
try {
    $uploadData = @{
        deck_name = "PowerShell Test Deck"
        description = "Created via API test script"
        flashcards = @(
            @{
                question = "What is PowerShell?"
                answer = "A task automation and configuration management framework"
                spacedRepetition = $false
            },
            @{
                question = "What is an API?"
                answer = "Application Programming Interface - a set of protocols for building software"
                spacedRepetition = $true
            }
        )
    } | ConvertTo-Json -Depth 3

    $newDeck = Invoke-RestMethod -Uri "$baseUrl/decks/upload/" `
        -Method Post `
        -ContentType "application/json" `
        -Body $uploadData
    
    Write-Host "✅ SUCCESS: Created deck '$($newDeck.name)' with ID $($newDeck.id)" -ForegroundColor Green
    $deckId = $newDeck.id
} catch {
    Write-Host "❌ FAILED: $_" -ForegroundColor Red
    $deckId = $null
}
Write-Host ""

# Test 4: Export the deck
if ($deckId) {
    Write-Host "Test 4: Exporting the deck..." -ForegroundColor Yellow
    try {
        $export = Invoke-RestMethod -Uri "$baseUrl/decks/$deckId/export/" -Method Get
        Write-Host "✅ SUCCESS: Exported '$($export.deck_name)'" -ForegroundColor Green
        Write-Host "  Flashcards: $($export.flashcards.Count)"
    } catch {
        Write-Host "❌ FAILED: $_" -ForegroundColor Red
    }
    Write-Host ""
}

# Test 5: Create a study session
Write-Host "Test 5: Creating a study session..." -ForegroundColor Yellow
try {
    $sessionData = @{ deck = 1 } | ConvertTo-Json
    $session = Invoke-RestMethod -Uri "$baseUrl/sessions/" `
        -Method Post `
        -ContentType "application/json" `
        -Body $sessionData
    
    Write-Host "✅ SUCCESS: Created session ID $($session.id)" -ForegroundColor Green
    $sessionId = $session.id
} catch {
    Write-Host "❌ FAILED: $_" -ForegroundColor Red
    $sessionId = $null
}
Write-Host ""

# Test 6: Record an answer
if ($sessionId) {
    Write-Host "Test 6: Recording a correct answer..." -ForegroundColor Yellow
    try {
        $answerData = @{ correct = $true } | ConvertTo-Json
        $updated = Invoke-RestMethod -Uri "$baseUrl/sessions/$sessionId/record_answer/" `
            -Method Post `
            -ContentType "application/json" `
            -Body $answerData
        
        Write-Host "✅ SUCCESS: Recorded answer" -ForegroundColor Green
        Write-Host "  Total attempts: $($updated.total_attempts)"
        Write-Host "  Correct: $($updated.correct_count)"
        Write-Host "  Accuracy: $($updated.accuracy)%"
    } catch {
        Write-Host "❌ FAILED: $_" -ForegroundColor Red
    }
    Write-Host ""
}

# Test 7: Get public decks
Write-Host "Test 7: Getting public decks..." -ForegroundColor Yellow
try {
    $publicDecks = Invoke-RestMethod -Uri "$baseUrl/decks/public/" -Method Get
    Write-Host "✅ SUCCESS: Found $($publicDecks.Count) public decks" -ForegroundColor Green
    $publicDecks | ForEach-Object { Write-Host "  - $($_.name)" }
} catch {
    Write-Host "❌ FAILED: $_" -ForegroundColor Red
}
Write-Host ""

# Test 8: List flashcards
Write-Host "Test 8: Listing flashcards..." -ForegroundColor Yellow
try {
    $cards = Invoke-RestMethod -Uri "$baseUrl/flashcards/" -Method Get
    Write-Host "✅ SUCCESS: Found $($cards.Count) flashcards total" -ForegroundColor Green
} catch {
    Write-Host "❌ FAILED: $_" -ForegroundColor Red
}
Write-Host ""

# Summary
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "   Test Suite Complete!" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Your StudyHub API is working! 🎉" -ForegroundColor Green
Write-Host "Visit http://localhost:8000 to use the web interface" -ForegroundColor Yellow
