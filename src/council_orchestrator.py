"""
Council Orchestrator for Healing Vault
Coordinates multiple friends responding to a journal entry
"""

from friend_personas import FRIENDS
from trigger_scorer import TriggerScorer
from advanced_rag import AdvancedRAG
from langchain_community.llms import Ollama

# Configuration
LLM_MODEL = "llama3.1:8b"


class CouncilOrchestrator:
    """Orchestrates multi-friend responses with RAG integration"""
    
    def __init__(self):
        """Initialize the council system"""
        print("=" * 70)
        print("HEALING VAULT - Council Initialization")
        print("=" * 70)
        
        # Initialize components
        self.scorer = TriggerScorer()
        self.rag = AdvancedRAG()
        self.llm = Ollama(model=LLM_MODEL, temperature=0.7)
        
        print("✓ Council of Friends ready\n")
    
    def generate_friend_response(self, friend_key, entry_text):
        """
        Generate a single friend's response with book citations
        
        Args:
            friend_key: Friend identifier
            entry_text: User's journal entry
            
        Returns:
            Friend's response text
        """
        friend = FRIENDS[friend_key]
        
        # Search books for relevant passages
        relevant_docs = self.rag.smart_search(
            entry_text, 
            top_k=3, 
            use_reranking=True
        )
        
        # Build context from retrieved passages
        context = "\n\n".join([
            f"From '{doc.metadata['book_title']}' (page {doc.metadata.get('page', '?')}):\n{doc.page_content[:400]}..."
            for doc, meta in relevant_docs
        ])
        
        # Build the prompt
        user_prompt = f"""Journal Entry:
"{entry_text}"

Relevant passages from psychology books:
{context}

Respond as {friend['name']} with your distinct voice and personality. Reference the books naturally when relevant. Keep response to 4-6 sentences."""
        
        full_prompt = f"{friend['system_prompt']}\n\n{user_prompt}"
        
        # Generate response
        response = self.llm.invoke(full_prompt)
        
        return response.strip()
    
    def process_entry(self, entry_text, threshold=70):
        """
        Process a journal entry and get council responses
        
        Args:
            entry_text: User's journal entry
            threshold: Minimum score for friend to respond
            
        Returns:
            Formatted multi-friend response
        """
        print("=" * 70)
        print("JOURNAL ENTRY:")
        print("=" * 70)
        print(entry_text)
        print("\n" + "=" * 70 + "\n")
        
        # Get triggered friends
        triggered = self.scorer.get_triggered_friends(entry_text, threshold)
        triggered = self.scorer.ensure_father_last(triggered)
        
        if not triggered:
            return "No friends were triggered above threshold. Try lowering the threshold or writing a more specific entry."
        
        # Generate responses
        responses = []
        
        for i, (friend_key, score) in enumerate(triggered, 1):
            friend = FRIENDS[friend_key]
            
            print(f"🧠 {friend['icon']} {friend['name']} is responding... ({i}/{len(triggered)})")
            
            response = self.generate_friend_response(friend_key, entry_text)
            
            responses.append({
                'friend': friend,
                'score': score,
                'response': response
            })
            
            print(f"✓ Response received\n")
        
        # Format final output
        output = self._format_responses(responses)
        
        return output
    
    def _format_responses(self, responses):
        """Format all responses into readable output"""
        output = []
        
        for resp in responses:
            friend = resp['friend']
            score = resp['score']
            text = resp['response']
            
            section = f"""{'─' * 70}

{friend['icon']} {friend['name'].upper()} (Relevance: {score}%)

{text}
"""
            output.append(section)
        
        return "\n".join(output) + "\n" + "─" * 70


def test_council():
    """Test the full council system"""
    council = CouncilOrchestrator()
    
    # Test entry
    test_entry = """I had a panic attack today when my boss raised his voice in the meeting. 
I couldn't breathe, my chest got tight, and I felt like I was going to pass out. 
I hate that I react this way - everyone else seemed fine but I just froze. 
I feel so weak and broken. God, why did you make me this way?"""
    
    # Process entry
    response = council.process_entry(test_entry, threshold=70)
    
    # Display results
    print("\n" + "=" * 70)
    print("COUNCIL RESPONSES:")
    print("=" * 70)
    print(response)


if __name__ == "__main__":
    test_council()