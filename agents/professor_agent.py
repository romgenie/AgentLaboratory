from agents.base_agent import BaseAgent


class ProfessorAgent(BaseAgent):
    """Agent that acts as a professor with deep academic knowledge."""
    
    def __init__(self, name, expertise, personality_traits, model):
        """Initialize a professor agent."""
        super().__init__(name, expertise, personality_traits, model)
        self.role = "Professor"
    
    def get_system_prompt(self):
        """
        Get the system prompt for this agent.
        
        Returns:
            str: System prompt
        """
        base_prompt = super().get_system_prompt()
        return (
            f"{base_prompt}\n\n"
            f"As a professor, you should prioritize academic rigor, theoretical depth, and research integrity. "
            f"Your responses should reflect deep knowledge of your field and attention to methodological details."
        )
    
    def evaluate_research_question(self, research_topic, research_question):
        """
        Evaluate a research question for academic merit.
        
        Args:
            research_topic (str): Research topic
            research_question (str): Research question to evaluate
            
        Returns:
            str: Evaluation and feedback
        """
        # This would call the LLM in a real implementation
        return f"Professor's analysis: This research question is significant and addresses an important gap in the literature."
    
    def review_literature(self, papers):
        """
        Review academic literature.
        
        Args:
            papers (list): List of papers to review
            
        Returns:
            str: Literature review insights
        """
        # This would process the papers and call the LLM in a real implementation
        return f"Literature review by {self.name}: The papers present significant findings in {self.expertise[0]}."
