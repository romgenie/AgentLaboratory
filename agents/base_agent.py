class BaseAgent:
    """Base class for all agents in the system."""
    
    def __init__(self, name, expertise, personality_traits, model):
        """
        Initialize a base agent.
        
        Args:
            name (str): Agent name
            expertise (list): List of expertise areas
            personality_traits (list): List of personality traits
            model (str): LLM model to use
        """
        self.name = name
        self.expertise = expertise
        self.personality_traits = personality_traits
        self.model = model
        self.memory = []
        self.conversation_history = []
    
    def get_response(self, prompt):
        """
        Get a response from the agent for the given prompt.
        
        Args:
            prompt (str): Input prompt
            
        Returns:
            str: Agent response
        """
        # In a real implementation, this would call the LLM
        # For testing, we'll return a simple response
        return f"Response from {self.name} about {prompt[:20]}..."
    
    def add_to_memory(self, prompt, response):
        """
        Add an interaction to the agent's memory.
        
        Args:
            prompt (str): Input prompt
            response (str): Agent response
            
        Returns:
            None
        """
        self.memory.append({"prompt": prompt, "response": response})
    
    def get_system_prompt(self):
        """
        Get the system prompt for this agent.
        
        Returns:
            str: System prompt
        """
        return (
            f"You are {self.name}, an AI assistant with expertise in {', '.join(self.expertise)}. "
            f"Your personality is characterized as {', '.join(self.personality_traits)}. "
            f"Respond to queries in a helpful and informative manner, consistent with your expertise and personality."
        )
    
    def analyze_approach(self, research_topic, aspect):
        """
        Analyze a research approach for a given topic and aspect.
        
        Args:
            research_topic (str): Research topic
            aspect (str): Aspect to analyze
            
        Returns:
            str: Analysis
        """
        # This would call the LLM in a real implementation
        return f"{self.name}'s analysis of {aspect} for {research_topic}"
