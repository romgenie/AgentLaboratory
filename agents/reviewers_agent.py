from agents.base_agent import BaseAgent


class ReviewersAgent(BaseAgent):
    """Agent that acts as a panel of reviewers providing feedback."""
    
    def __init__(self, name, expertise, personality_traits, model):
        """Initialize a reviewers agent."""
        super().__init__(name, expertise, personality_traits, model)
        self.role = "Reviewers Panel"
    
    def get_system_prompt(self):
        """
        Get the system prompt for this agent.
        
        Returns:
            str: System prompt
        """
        base_prompt = super().get_system_prompt()
        return (
            f"{base_prompt}\n\n"
            f"As a panel of reviewers, you should provide balanced, constructive feedback "
            f"from multiple perspectives. Your responses should identify strengths, weaknesses, "
            f"and potential improvements in research plans and methodologies."
        )
    
    def review_proposal(self, research_topic, research_question, professor_feedback=None, student_proposal=None):
        """
        Review a research proposal.
        
        Args:
            research_topic (str): Research topic
            research_question (str): Research question
            professor_feedback (str, optional): Feedback from professor
            student_proposal (str, optional): Proposal from student
            
        Returns:
            str: Review feedback
        """
        # This would call the LLM in a real implementation
        return f"Reviewer's feedback: The approach is sound but needs more rigorous evaluation."
    
    def evaluate_research(self, research_results):
        """
        Evaluate research results.
        
        Args:
            research_results (dict): Research results to evaluate
            
        Returns:
            str: Evaluation feedback
        """
        # This would call the LLM in a real implementation
        return f"Evaluation by {self.name}: The research demonstrates significant findings with some limitations."
