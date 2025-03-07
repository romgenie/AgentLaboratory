from agents.base_agent import BaseAgent


class MLEngineerAgent(BaseAgent):
    """Agent that acts as a machine learning engineer."""
    
    def __init__(self, name, expertise, personality_traits, model):
        """Initialize a machine learning engineer agent."""
        super().__init__(name, expertise, personality_traits, model)
        self.role = "ML Engineer"
    
    def get_system_prompt(self):
        """
        Get the system prompt for this agent.
        
        Returns:
            str: System prompt
        """
        base_prompt = super().get_system_prompt()
        return (
            f"{base_prompt}\n\n"
            f"As a machine learning engineer, you should focus on designing and implementing effective ML models. "
            f"Your responses should demonstrate expertise in model selection, feature engineering, hyperparameter tuning, "
            f"and evaluation methodologies."
        )
    
    def design_model(self, requirements, data_description):
        """
        Design a machine learning model.
        
        Args:
            requirements (str): Requirements specification
            data_description (str): Description of the data
            
        Returns:
            str: Model design
        """
        # This would call the LLM in a real implementation
        return f"Model design by {self.name}: A neural network architecture with the following layers..."
    
    def evaluate_results(self, model_results):
        """
        Evaluate machine learning model results.
        
        Args:
            model_results (dict): Results to evaluate
            
        Returns:
            str: Evaluation
        """
        # This would call the LLM in a real implementation
        return f"Evaluation by {self.name}: The model achieves 92% accuracy but shows signs of overfitting on the validation set."
