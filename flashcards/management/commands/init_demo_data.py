"""
Initial data setup for demo decks
"""
from django.core.management.base import BaseCommand
from flashcards.models import Deck, Flashcard


class Command(BaseCommand):
    help = 'Create initial demo flashcard decks'

    def handle(self, *args, **options):
        # Create Biology deck
        biology_deck, created = Deck.objects.get_or_create(
            name='Biology 101',
            defaults={
                'description': 'Essential biology concepts for beginners',
                'is_public': True
            }
        )
        
        if created:
            biology_cards = [
                {
                    'question': 'What is the powerhouse of the cell?',
                    'answer': 'Mitochondria - they produce ATP through cellular respiration',
                    'spaced_repetition': True
                },
                {
                    'question': 'What is photosynthesis?',
                    'answer': 'The process by which plants convert sunlight, water, and CO₂ into glucose and oxygen',
                    'spaced_repetition': True
                },
                {
                    'question': 'What is DNA?',
                    'answer': 'Deoxyribonucleic acid - the molecule that carries genetic information',
                    'spaced_repetition': False
                },
                {
                    'question': 'What are the three types of RNA?',
                    'answer': 'mRNA (messenger), tRNA (transfer), and rRNA (ribosomal)',
                    'spaced_repetition': True
                },
            ]
            
            for idx, card_data in enumerate(biology_cards):
                Flashcard.objects.create(
                    deck=biology_deck,
                    question=card_data['question'],
                    answer=card_data['answer'],
                    spaced_repetition=card_data['spaced_repetition'],
                    order=idx
                )
            
            self.stdout.write(self.style.SUCCESS(f'Created Biology deck with {len(biology_cards)} cards'))

        # Create Chemistry deck
        chemistry_deck, created = Deck.objects.get_or_create(
            name='Chemistry Basics',
            defaults={
                'description': 'Fundamental chemistry concepts',
                'is_public': True
            }
        )
        
        if created:
            chemistry_cards = [
                {
                    'question': 'What is the chemical symbol for water?',
                    'answer': 'H₂O - Two hydrogen atoms bonded to one oxygen atom',
                    'spaced_repetition': False
                },
                {
                    'question': 'What is an atom?',
                    'answer': 'The smallest unit of matter that retains the properties of an element',
                    'spaced_repetition': True
                },
                {
                    'question': 'What is the periodic table?',
                    'answer': 'A tabular arrangement of chemical elements organized by atomic number',
                    'spaced_repetition': False
                },
            ]
            
            for idx, card_data in enumerate(chemistry_cards):
                Flashcard.objects.create(
                    deck=chemistry_deck,
                    question=card_data['question'],
                    answer=card_data['answer'],
                    spaced_repetition=card_data['spaced_repetition'],
                    order=idx
                )
            
            self.stdout.write(self.style.SUCCESS(f'Created Chemistry deck with {len(chemistry_cards)} cards'))

        # Create History deck
        history_deck, created = Deck.objects.get_or_create(
            name='World History',
            defaults={
                'description': 'Important historical events and figures',
                'is_public': True
            }
        )
        
        if created:
            history_cards = [
                {
                    'question': 'Who wrote "Romeo and Juliet"?',
                    'answer': 'William Shakespeare - written around 1594-1596',
                    'spaced_repetition': False
                },
                {
                    'question': 'When did World War II end?',
                    'answer': 'September 2, 1945 - when Japan formally surrendered',
                    'spaced_repetition': True
                },
            ]
            
            for idx, card_data in enumerate(history_cards):
                Flashcard.objects.create(
                    deck=history_deck,
                    question=card_data['question'],
                    answer=card_data['answer'],
                    spaced_repetition=card_data['spaced_repetition'],
                    order=idx
                )
            
            self.stdout.write(self.style.SUCCESS(f'Created History deck with {len(history_cards)} cards'))

        self.stdout.write(self.style.SUCCESS('Successfully initialized demo data!'))
