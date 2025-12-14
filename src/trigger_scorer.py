"""
Trigger Scoring System for Healing Vault
Analyzes journal entries and scores which friends should respond
"""

from friend_personas import FRIENDS
from langchain_community.embeddings import OllamaEmbeddings

# Configuration
EMBEDDING_MODEL = "llama3.1:8b"
TRIGGER_THRESHOLD = 70  # Friends scoring above this will respond


class TriggerScorer:
    """Scores which friends should respond to a journal entry"""
    
    def __init__(self):
        """Initialize the scorer"""
        print("🎯 Initializing trigger scorer...")
        self.embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
        print("✓ Trigger scorer ready\n")
    
    def score_friend(self, entry_text, friend_key):
        """
        Score a single friend's relevance to the entry
        
        Args:
            entry_text: User's journal entry
            friend_key: Friend identifier (e.g., 'trauma_guide')
            
        Returns:
            Score from 0-100
        """
        friend = FRIENDS[friend_key]
        entry_lower = entry_text.lower()
        
        # Keyword matching (60% of score)
        keyword_score = 0
        trigger_words = friend['triggers']
        
        for trigger in trigger_words:
            # Count occurrences of trigger word
            count = entry_lower.count(trigger.lower())
            if count > 0:
                # First occurrence = 10 points, additional = 5 each
                keyword_score += 10 + (count - 1) * 5
        
        # Normalize to 0-60 range
        keyword_score = min(60, keyword_score)
        
        # Semantic similarity (40% of score)
        # Check if entry semantically matches friend's domain
        domain_keywords = " ".join(trigger_words[:10])  # Use top 10 triggers
        
        try:
            entry_embedding = self.embeddings.embed_query(entry_text)
            domain_embedding = self.embeddings.embed_query(domain_keywords)
            
            # Calculate cosine similarity
            import numpy as np
            similarity = np.dot(entry_embedding, domain_embedding) / (
                np.linalg.norm(entry_embedding) * np.linalg.norm(domain_embedding)
            )
            
            # Convert to 0-40 range
            semantic_score = max(0, min(40, similarity * 100))
        except:
            # If embedding fails, use keyword score only
            semantic_score = 0
        
        total_score = keyword_score + semantic_score
        return round(total_score, 1)
    
    def get_triggered_friends(self, entry_text, threshold=TRIGGER_THRESHOLD):
        """
        Get all friends who should respond to this entry
        
        Args:
            entry_text: User's journal entry
            threshold: Minimum score for friend to respond
            
        Returns:
            List of (friend_key, score) tuples, sorted by score (highest first)
        """
        print(f"📊 Scoring all friends for this entry...")
        
        scores = []
        for friend_key in FRIENDS.keys():
            score = self.score_friend(entry_text, friend_key)
            scores.append((friend_key, score))
            
            friend_name = FRIENDS[friend_key]['name']
            icon = FRIENDS[friend_key]['icon']
            print(f"  {icon} {friend_name}: {score}%")
        
        # Sort by score (highest first)
        scores.sort(key=lambda x: x[1], reverse=True)
        
        # Filter to only those above threshold
        triggered = [(key, score) for key, score in scores if score >= threshold]
        
        print(f"\n✓ {len(triggered)} friends will respond (threshold: {threshold}%)\n")
        
        return triggered
    
    def ensure_father_last(self, triggered_friends):
        """
        Ensure Gentle Father speaks last if he's triggered
        
        Args:
            triggered_friends: List of (friend_key, score) tuples
            
        Returns:
            Reordered list with gentle_father at the end if present
        """
        # Check if Gentle Father is in the list
        father_entry = None
        other_friends = []
        
        for friend_key, score in triggered_friends:
            if friend_key == "gentle_father":
                father_entry = (friend_key, score)
            else:
                other_friends.append((friend_key, score))
        
        # If Father is triggered, put him last
        if father_entry:
            return other_friends + [father_entry]
        else:
            return other_friends


def test_scorer():
    """Test the trigger scorer with sample entries"""
    scorer = TriggerScorer()
    
    test_entries = [
        {
            "name": "Panic Attack Entry",
            "text": """I had a panic attack today when my boss raised his voice in the meeting. 
            I couldn't breathe, my chest got tight, and I felt like I was going to pass out. 
            I hate that I react this way - everyone else seemed fine but I just froze. 
            I feel so weak and broken."""
        },
        {
            "name": "Relationship Anxiety Entry",
            "text": """My partner said they needed space tonight and I immediately panicked. 
            I started texting them over and over asking if we're okay, if they're mad at me. 
            I know I'm being clingy but I can't help it - I'm terrified they're going to leave. 
            I feel like I'm suffocating them with my neediness."""
        },
        {
            "name": "Shame & Identity Entry",
            "text": """I keep messing up at work and I feel like such a failure. 
            I'm supposed to be a good Christian but I can't even get my life together. 
            God must be so disappointed in me. I don't deserve grace - I need to try harder 
            and be better. Maybe if I just pray more and read my Bible more I'll finally 
            be worthy of His love."""
        }
    ]
    
    for entry in test_entries:
        print("=" * 70)
        print(f"TEST ENTRY: {entry['name']}")
        print("=" * 70)
        print(f"{entry['text']}\n")
        
        triggered = scorer.get_triggered_friends(entry['text'])
        triggered = scorer.ensure_father_last(triggered)
        
        print("FINAL RESPONSE ORDER:")
        for i, (friend_key, score) in enumerate(triggered, 1):
            friend = FRIENDS[friend_key]
            print(f"{i}. {friend['icon']} {friend['name']} ({score}%)")
        
        print("\n" + "-" * 70 + "\n")


if __name__ == "__main__":
    test_scorer()