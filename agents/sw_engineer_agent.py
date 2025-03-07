from agents.base_agent import BaseAgent


class SWEngineerAgent(BaseAgent):
    """Agent that acts as a software engineer with coding expertise."""
    
    def __init__(self, name, expertise, personality_traits, model):
        """Initialize a software engineer agent."""
        super().__init__(name, expertise, personality_traits, model)
        self.role = "Software Engineer"
    
    def get_system_prompt(self):
        """
        Get the system prompt for this agent.
        
        Returns:
            str: System prompt
        """
        base_prompt = super().get_system_prompt()
        return (
            f"{base_prompt}\n\n"
            f"As a software engineer, you should prioritize code quality, efficiency, and maintainability. "
            f"Your responses should provide well-structured, documented code solutions and consider "
            f"best practices in software development."
        )
    
    def write_code(self, requirements, language="python"):
        """
        Write code based on requirements.
        
        Args:
            requirements (str): Requirements specification
            language (str): Programming language
            
        Returns:
            str: Code implementation
        """
        # This would call the LLM in a real implementation
        return f"```{language}\n# Implementation by {self.name}\ndef main():\n    print('Hello, world!')\n```"
    
    def refactor_code(self, code):
        """
        Refactor existing code.
        
        Args:
            code (str): Code to refactor
            
        Returns:
            str: Refactored code
        """
        # This would call the LLM in a real implementation
        return f"Refactored code:\n```python\n# Refactored by {self.name}\ndef improved_main():\n    print('Hello, optimized world!')\n```"
