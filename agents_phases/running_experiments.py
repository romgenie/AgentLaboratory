class RunningExperiments:
    """Running experiments phase of the research process."""
    
    def __init__(self, sw_engineer_agent, ml_engineer_agent, research_topic, research_plan, research_dir):
        """
        Initialize the running experiments phase.
        
        Args:
            sw_engineer_agent: Software engineer agent
            ml_engineer_agent: ML engineer agent
            research_topic (str): Research topic
            research_plan (dict): Research plan
            research_dir (str): Research directory path
        """
        self.sw_engineer_agent = sw_engineer_agent
        self.ml_engineer_agent = ml_engineer_agent
        self.research_topic = research_topic
        self.research_plan = research_plan
        self.research_dir = research_dir
    
    def execute(self):
        """
        Execute the running experiments phase.
        
        Returns:
            dict: Experiment results
        """
        # Design experiments
        experiment_designs = self.design_experiments()
        
        # Implement code
        code = self.implement_code(experiment_designs)
        
        # Execute experiments
        results = self.execute_experiments(code)
        
        # Analyze results
        analysis = self.analyze_results(results)
        
        # Return results
        return {
            "experiment_designs": experiment_designs,
            "code": code,
            "results": results,
            "analysis": analysis
        }
    
    def design_experiments(self):
        """
        Design experiments based on the research plan.
        
        Returns:
            list: Experiment designs
        """
        # This would use the ml engineer agent to design experiments
        return [
            "Experiment setup 1: Baseline model with default parameters",
            "Experiment setup 2: Proposed model with optimized parameters"
        ]
    
    def implement_code(self, experiment_designs):
        """
        Implement code for the experiments.
        
        Args:
            experiment_designs (list): Experiment designs
            
        Returns:
            str: Implemented code
        """
        # This would use the sw engineer agent to implement code
        return "# Implemented code for experiments\nimport numpy as np\nimport sklearn\n# Model implementation..."
    
    def execute_experiments(self, code):
        """
        Execute experiments with the implemented code.
        
        Args:
            code (str): Implemented code
            
        Returns:
            dict: Experiment results
        """
        # This would use code_executor to run the code
        return {
            "experiment1": {"accuracy": 0.85, "f1": 0.83, "runtime": 120},
            "experiment2": {"accuracy": 0.92, "f1": 0.91, "runtime": 150}
        }
    
    def analyze_results(self, results):
        """
        Analyze experimental results.
        
        Args:
            results (dict): Experiment results
            
        Returns:
            str: Analysis
        """
        # This would use the ml engineer agent to analyze results
        return "The proposed model outperforms the baseline by 7% in accuracy and 8% in F1 score, with a 25% increase in runtime."
    
    def save_results(self, results):
        """
        Save the experiment results.
        
        Args:
            results (dict): Results to save
            
        Returns:
            None
        """
        # This would save the results to the research directory
        import os
        import json
        
        # Create output file path
        output_file = os.path.join(self.research_dir, "experiment_results.json")
        
        # Save results
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)
