from agents.base_agent import BaseAgent


class PhDStudentAgent(BaseAgent):
    """Agent that acts as a PhD student with research skills."""
    
    def __init__(self, name, expertise, personality_traits, model):
        """Initialize a PhD student agent."""
        super().__init__(name, expertise, personality_traits, model)
        self.role = "PhD Student"
    
    def get_system_prompt(self):
        """
        Get the system prompt for this agent.
        
        Returns:
            str: System prompt
        """
        base_prompt = super().get_system_prompt()
        return (
            f"{base_prompt}\n\n"
            f"As a PhD student, you should demonstrate deep understanding of research methodologies "
            f"and a willingness to explore innovative approaches. Your responses should reflect "
            f"your growing expertise and your commitment to rigorous scholarship."
        )
    
    def propose_methodology(self, research_topic, research_question, professor_feedback=None):
        """
        Propose a research methodology for a given question.
        
        Args:
            research_topic (str): Research topic
            research_question (str): Research question
            professor_feedback (str, optional): Feedback from professor to incorporate
            
        Returns:
            str: Proposed methodology
        """
        # This would call the LLM in a real implementation
        return f"PhD Student's analysis: I believe we should focus on methodology X for best results."
    
    def search_literature(self, keywords):
        """
        Search for relevant literature based on keywords.
        
        Args:
            keywords (list): Keywords to search for
            
        Returns:
            str: Literature search results
        """
        # This would use search tools and call the LLM in a real implementation
        return f"Literature search by {self.name}: Found relevant papers on {', '.join(keywords)}."
