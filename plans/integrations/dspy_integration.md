# AgentLaboratory + DSPy Integration Plan

## Overview

This document outlines the comprehensive plan for integrating DSPy into the AgentLaboratory codebase. DSPy is a framework for programming—rather than prompting—language models, which will enable significant improvements to the AgentLaboratory system:

1. **Enhanced Agent Optimization**: Replace manual prompt engineering with DSPy's automated optimization
2. **Structured I/O**: Move from text-based interactions to structured input/output specifications
3. **Improved Performance**: Leverage DSPy's optimization to improve agent performance across phases
4. **Maintainable Architecture**: Create more modular and maintainable agent code structure 

## Architecture Changes

### High-Level Design Changes

1. **Model Interaction Layer**:
   - Replace direct LLM API calls with DSPy's model abstraction
   - Maintain token usage tracking and cost estimation

2. **Agent Architecture**:
   - Replace the current text-based prompting patterns with DSPy Modules
   - Define Signatures for structured I/O between agents
   - Maintain agent state management while leveraging DSPy's composition ability

3. **Workflow Orchestration**:
   - Adapt the LaboratoryWorkflow class to work with DSPy modules
   - Add optimization capabilities at each phase
   - Support both legacy and DSPy-powered agents for backward compatibility

4. **Optimization Framework**:
   - Implement DSPy metrics for each research phase
   - Create optimization strategies that work across agent interactions
   - Build custom optimization loops for complex multi-agent workflows

## Implementation Plan

### Phase 1: Core Infrastructure

#### Create DSPy Configuration (New File: `dspy_config.py`)

```python
import dspy
import os
from typing import Dict, Any, Optional

# Configure DSPy with default settings
def configure_dspy(model_name: str = "gpt-4o-mini", api_key: Optional[str] = None) -> None:
    """Configure DSPy with the specified model and settings."""
    if api_key is None:
        api_key = os.getenv('OPENAI_API_KEY')
    
    if model_name.startswith("gpt"):
        dspy.configure(lm=dspy.OpenAI(model=model_name, api_key=api_key))
    elif model_name == "deepseek-chat":
        dspy.configure(lm=dspy.DeepseekAI(model=model_name, api_key=os.getenv('DEEPSEEK_API_KEY')))
    elif model_name.startswith("claude"):
        dspy.configure(lm=dspy.Anthropic(model=model_name, api_key=os.getenv('ANTHROPIC_API_KEY')))
    # Add more model configurations as needed
    
# Model mapping for easy reference
MODEL_MAPPING = {
    "gpt-4o": "gpt-4o-2024-08-06",
    "gpt-4o-mini": "gpt-4o-mini-2024-07-18",
    "o1-preview": "o1-preview",
    "o1-mini": "o1-mini-2024-09-12",
    "o1": "o1-2024-12-17",
    "claude-3-5-sonnet": "claude-3-5-sonnet-latest",
    "deepseek-chat": "deepseek-chat"
}

# Track token usage similarly to the original implementation
TOKEN_TRACKER = {
    "tokens_in": {},
    "tokens_out": {}
}
```

#### Update Inference Module (Update File: `inference.py`)

Create a DSPy-compatible version of the query_model function that maintains the same interface:

```python
import time, tiktoken
from openai import OpenAI
import openai
import os, anthropic, json
import dspy
from dspy_config import configure_dspy, MODEL_MAPPING, TOKEN_TRACKER

# Maintain the original token tracking
TOKENS_IN = dict()
TOKENS_OUT = dict()
encoding = tiktoken.get_encoding("cl100k_base")

def curr_cost_est():
    # Keep the original cost estimation function
    # ...

def query_model_dspy(model_str, prompt, system_prompt, openai_api_key=None, anthropic_api_key=None, 
               tries=5, timeout=5.0, temp=None, print_cost=True):
    """DSPy-powered version of query_model that maintains the same interface."""
    preloaded_api = os.getenv('OPENAI_API_KEY')
    if openai_api_key is None and preloaded_api is not None:
        openai_api_key = preloaded_api
        
    # Configure DSPy with the appropriate model
    configure_dspy(MODEL_MAPPING.get(model_str, model_str), openai_api_key)
    
    # Create a simple DSPy module for this request
    class SimpleQuery(dspy.Module):
        def __init__(self, system_prompt):
            self.system_prompt = system_prompt
            self.predictor = dspy.Predict("user_query -> assistant_response")
            
        def forward(self, user_query):
            # Inject system prompt into the context
            dspy.context(system=self.system_prompt)
            return self.predictor(user_query=user_query)
    
    # Create the module and run inference
    module = SimpleQuery(system_prompt)
    
    for _ in range(tries):
        try:
            result = module(prompt)
            answer = result.assistant_response
            
            # Update token tracking
            try:
                if model_str not in TOKENS_IN:
                    TOKENS_IN[model_str] = 0
                    TOKENS_OUT[model_str] = 0
                
                # Estimate token counts (this is approximate)
                TOKENS_IN[model_str] += len(encoding.encode(system_prompt + prompt))
                TOKENS_OUT[model_str] += len(encoding.encode(answer))
                
                if print_cost:
                    print(f"Current experiment cost = ${curr_cost_est()}, ** Approximate values, may not reflect true cost")
            except Exception as e:
                if print_cost:
                    print(f"Cost approximation has an error? {e}")
                    
            return answer
            
        except Exception as e:
            print("Inference Exception:", e)
            time.sleep(timeout)
            continue
            
    raise Exception("Max retries: timeout")
    
# Keep the original function for backward compatibility
# query_model = ...
```

### Phase 2: Agent Modules Implementation

#### Create Base Agent Modules (New File: `dspy_modules/agent_modules.py`)

```python
import dspy
from typing import List, Dict, Any, Optional

class BaseAgentModule(dspy.Module):
    """Base DSPy module for all AgentLaboratory agents."""
    
    def __init__(self, role: str, notes: List[Dict[str, Any]] = None):
        self.role = role
        self.notes = notes or []
        self.state = {}
        
        # Define the basic signature for agent interactions
        self.predictor = dspy.ChainOfThought(
            "research_topic, phase, step, feedback -> agent_response"
        )
        
    def forward(self, research_topic: str, phase: str, step: int = 0, feedback: str = ""):
        """Run inference with the agent."""
        # Filter notes relevant to the current phase
        relevant_notes = [
            note["note"] for note in self.notes 
            if "phases" in note and phase in note["phases"]
        ]
        notes_text = "\n".join(relevant_notes) if relevant_notes else ""
        
        # Prepare context with role information and notes
        context = f"You are a {self.role}. Your task is to help with the research phase: {phase}."
        if notes_text:
            context += f"\n\nNotes for this task:\n{notes_text}"
            
        # Set the context for DSPy
        dspy.context(system=context)
        
        # Run the prediction
        result = self.predictor(
            research_topic=research_topic,
            phase=phase,
            step=step,
            feedback=feedback
        )
        
        return result.agent_response
        
# Define specific agent modules
class PhDStudentModule(BaseAgentModule):
    """DSPy module for PhD Student agent."""
    
    def __init__(self, notes=None):
        super().__init__(role="PhD Student Researcher", notes=notes)
        self.lit_review = []
        self.lit_review_sum = ""
        
    # Add specialized methods for literature review, etc.
    
class ProfessorModule(BaseAgentModule):
    """DSPy module for Professor agent."""
    
    def __init__(self, notes=None):
        super().__init__(role="Professor and Research Supervisor", notes=notes)
        
    # Add specialized methods for reviewing, etc.

# Add other agent modules...
```

#### Create Phase-Specific Modules (New File: `dspy_modules/phase_modules.py`)

```python
import dspy
from typing import List, Dict, Any, Optional

class LiteratureReviewModule(dspy.Module):
    """DSPy module for Literature Review phase."""
    
    def __init__(self):
        # Define the signature for literature review activities
        self.paper_finder = dspy.ChainOfThought("research_topic -> search_query")
        self.paper_selector = dspy.ChainOfThought("paper_summaries, research_topic -> selected_papers")
        self.paper_reviewer = dspy.ChainOfThought("paper_text, research_topic -> paper_review")
        self.review_summarizer = dspy.ChainOfThought("paper_reviews -> literature_review_summary")
        
    def find_papers(self, research_topic: str):
        """Generate search queries for the research topic."""
        result = self.paper_finder(research_topic=research_topic)
        return result.search_query
        
    def select_papers(self, paper_summaries: str, research_topic: str):
        """Select relevant papers from summaries."""
        result = self.paper_selector(
            paper_summaries=paper_summaries,
            research_topic=research_topic
        )
        return result.selected_papers
        
    def review_paper(self, paper_text: str, research_topic: str):
        """Review a specific paper."""
        result = self.paper_reviewer(
            paper_text=paper_text,
            research_topic=research_topic
        )
        return result.paper_review
        
    def summarize_reviews(self, paper_reviews: List[str]):
        """Summarize all paper reviews into a final literature review."""
        reviews_text = "\n\n".join(paper_reviews)
        result = self.review_summarizer(paper_reviews=reviews_text)
        return result.literature_review_summary

# Add other phase modules...
```

#### Create Custom Metrics (New File: `dspy_modules/metrics.py`)

```python
import dspy
from typing import Any, Dict, List, Optional

class LiteratureReviewMetric(dspy.Metric):
    """Evaluates the quality of a literature review."""
    
    def __init__(self):
        self.evaluator = dspy.ChainOfThought(
            "literature_review, research_topic -> score, feedback"
        )
        
    def score(self, 
              gold: Dict[str, Any], 
              pred: Dict[str, Any], 
              trace: Optional[List[Dict[str, Any]]] = None) -> float:
        """Score a literature review on a scale of 0-1."""
        result = self.evaluator(
            literature_review=pred["literature_review_summary"],
            research_topic=gold["research_topic"]
        )
        
        try:
            score = float(result.score.strip())
            # Normalize to 0-1 if needed
            return min(max(score / 10.0, 0.0), 1.0)
        except:
            return 0.0

class ExperimentQualityMetric(dspy.Metric):
    """Evaluates the quality of experimental code and results."""
    
    def __init__(self):
        self.evaluator = dspy.ChainOfThought(
            "code, results, research_plan -> score, feedback"
        )
        
    def score(self, 
              gold: Dict[str, Any], 
              pred: Dict[str, Any], 
              trace: Optional[List[Dict[str, Any]]] = None) -> float:
        """Score an experiment on a scale of 0-1."""
        result = self.evaluator(
            code=pred["code"],
            results=pred["results"],
            research_plan=gold["research_plan"]
        )
        
        try:
            score = float(result.score.strip())
            return min(max(score / 10.0, 0.0), 1.0)
        except:
            return 0.0

# Add other metrics...
```

### Phase 3: Update Agent Classes

#### Update Base Agent (Update File: `agents/base_agent.py`)

```python
from common_imports import *
from inference import query_model, query_model_dspy
from dspy_modules.agent_modules import BaseAgentModule

class BaseAgent:
    """Base agent class with DSPy integration."""
    
    def __init__(self, model="gpt-4o-mini", notes=list(), max_steps=10, openai_api_key=None):
        self.model = model
        self.notes = notes
        self.max_steps = max_steps
        self.openai_api_key = openai_api_key
        self.reset()
        
        # Create the DSPy module for this agent
        self._create_dspy_module()
        
    def _create_dspy_module(self):
        """Create the DSPy module for this agent. Override in subclasses."""
        self.dspy_module = BaseAgentModule(role=self.__class__.__name__, notes=self.notes)
        
    def reset(self):
        """Reset agent state."""
        self.plan = ""
        self.lit_review = []
        self.lit_review_sum = ""
        self.dataset_code = ""
        self.results_code = ""
        self.exp_results = ""
        self.interpretation = ""
        self.report = ""
        self.second_round = False
        
    def inference(self, research_topic, phase, feedback="", step=0, temp=None):
        """Run inference with this agent, using DSPy if available."""
        try:
            # Try using the DSPy module first
            return self.dspy_module(
                research_topic=research_topic,
                phase=phase,
                step=step,
                feedback=feedback
            )
        except Exception as e:
            print(f"DSPy inference failed, falling back to traditional approach: {e}")
            # Fall back to the original approach
            system_prompt = self.get_system_prompt(phase, step)
            prompt = self.get_prompt(research_topic, phase, feedback, step)
            return query_model(
                model_str=self.model, 
                prompt=prompt, 
                system_prompt=system_prompt,
                openai_api_key=self.openai_api_key,
                temp=temp
            )
    
    def get_system_prompt(self, phase, step):
        """Get system prompt for this agent. Override in subclasses."""
        return f"You are a {self.__class__.__name__}."
        
    def get_prompt(self, research_topic, phase, feedback, step):
        """Get user prompt for this agent. Override in subclasses."""
        return f"Research topic: {research_topic}\nPhase: {phase}\nStep: {step}\nFeedback: {feedback}"
    
    # Add other base agent methods...
```

#### Update Specific Agents (e.g., Update File: `agents/phd_student_agent.py`)

```python
from agents.base_agent import BaseAgent
from dspy_modules.agent_modules import PhDStudentModule
from common_imports import *

class PhDStudentAgent(BaseAgent):
    """PhD Student Agent with DSPy integration."""
    
    def _create_dspy_module(self):
        """Create the PhD Student DSPy module."""
        self.dspy_module = PhDStudentModule(notes=self.notes)
        
    def get_system_prompt(self, phase, step):
        """Legacy system prompt for compatibility."""
        # Original system prompt...
        
    def get_prompt(self, research_topic, phase, feedback, step):
        """Legacy prompt for compatibility."""
        # Original prompt...
        
    def add_review(self, paper_id, arxiv_engine):
        """Add a paper to the literature review."""
        # Either use DSPy module or original implementation...
        
    def format_review(self):
        """Format the literature review."""
        # Either use DSPy module or original implementation...
        
    # Add other specialized methods...
```

### Phase 4: Update Workflow Orchestration

#### Update Laboratory Workflow (Update File: `ai_lab_repo.py`)

Modify the `LaboratoryWorkflow` class to support DSPy optimization:

```python
# Add imports for DSPy
from dspy_modules.phase_modules import *
from dspy_modules.metrics import *
import dspy

class LaboratoryWorkflow:
    def __init__(self, research_topic, openai_api_key, max_steps=100, 
                 num_papers_lit_review=5, agent_model_backbone=f"{DEFAULT_LLM_BACKBONE}", 
                 notes=list(), human_in_loop_flag=None, compile_pdf=True, 
                 mlesolver_max_steps=3, papersolver_max_steps=5, use_dspy=True):
        # Original initialization
        # ...
        
        # Add DSPy flag and modules
        self.use_dspy = use_dspy
        if self.use_dspy:
            self._initialize_dspy_modules()
            
    def _initialize_dspy_modules(self):
        """Initialize DSPy modules for each phase."""
        self.dspy_modules = {
            "literature review": LiteratureReviewModule(),
            "plan formulation": PlanFormulationModule(),
            "data preparation": DataPreparationModule(),
            "running experiments": ExperimentModule(),
            "results interpretation": ResultsInterpretationModule(),
            "report writing": ReportWritingModule(),
            "report refinement": ReportRefinementModule(),
        }
        
        # Initialize metrics
        self.dspy_metrics = {
            "literature review": LiteratureReviewMetric(),
            "plan formulation": PlanFormulationMetric(),
            "data preparation": DataQualityMetric(),
            "running experiments": ExperimentQualityMetric(),
            "results interpretation": InterpretationMetric(),
            "report writing": ReportQualityMetric(),
            "report refinement": ReviewResponseMetric(),
        }
        
    def optimize_phase(self, phase, trainset=None):
        """Apply DSPy optimization to a specific phase."""
        if not self.use_dspy or phase not in self.dspy_modules:
            return
            
        if trainset is None:
            # Create a minimal trainset from previous runs or examples
            trainset = [dspy.Example(research_topic=self.research_topic)]
            
        # Optimize the module
        optimizer = dspy.MIPROv2(
            metric=self.dspy_metrics[phase],
            auto="light",
            num_threads=4
        )
        
        optimized_module = optimizer.compile(
            self.dspy_modules[phase],
            trainset=trainset
        )
        
        # Replace the original module
        self.dspy_modules[phase] = optimized_module
        
    # Update each phase method to use DSPy if enabled
    def literature_review(self):
        """Perform literature review with DSPy if enabled."""
        if self.use_dspy:
            # Use DSPy modules for this phase
            # ...
        else:
            # Original implementation
            # ...
            
    # Update other phase methods similarly...
```

### Phase 5: Implement Custom Optimizers

#### Create Custom Optimizer (New File: `dspy_optimizers.py`)

```python
import dspy
from typing import Dict, List, Any, Optional, Callable

class MultiAgentOptimizer(dspy.Optimizer):
    """Custom optimizer for multi-agent workflows."""
    
    def __init__(self, 
                 agents: Dict[str, dspy.Module],
                 metric: dspy.Metric,
                 max_iterations: int = 5):
        self.agents = agents
        self.metric = metric
        self.max_iterations = max_iterations
        
    def compile(self, 
                program: dspy.Module, 
                trainset: List[Dict[str, Any]], 
                valset: Optional[List[Dict[str, Any]]] = None) -> dspy.Module:
        """Optimize a multi-agent workflow."""
        # Implementation of multi-agent optimization
        # ...
        
class MLESolverOptimizer(dspy.Optimizer):
    """Optimizer for the MLESolver class."""
    
    def __init__(self, 
                 metric: Callable,
                 max_steps: int = 3):
        self.metric = dspy.Metric(metric)
        self.max_steps = max_steps
        
    def compile(self, 
                program: dspy.Module, 
                trainset: List[Dict[str, Any]], 
                valset: Optional[List[Dict[str, Any]]] = None) -> dspy.Module:
        """Optimize an MLESolver-based workflow."""
        # Implementation of MLESolver optimization
        # ...
```

### Phase 6: Update Solvers

#### Update MLESolver (Update File: `mlesolver.py`)

```python
import dspy
from dspy_optimizers import MLESolverOptimizer
from dspy_modules.metrics import ExperimentQualityMetric
from common_imports import *

class MLESolver:
    """MLESolver with DSPy integration."""
    
    def __init__(self, dataset_code, notes="", insights="", 
                 max_steps=3, plan="", openai_api_key=None, 
                 llm_str="gpt-4o-mini", use_dspy=True):
        self.dataset_code = dataset_code
        self.notes = notes
        self.insights = insights
        self.max_steps = max_steps
        self.plan = plan
        self.openai_api_key = openai_api_key
        self.llm_str = llm_str
        self.use_dspy = use_dspy
        
        self.best_codes = []
        
        if self.use_dspy:
            self._initialize_dspy_modules()
            
    def _initialize_dspy_modules(self):
        """Initialize DSPy modules for MLESolver."""
        # Create the code generation module
        class CodeGenerator(dspy.Module):
            def __init__(self):
                self.generator = dspy.ChainOfThought(
                    "dataset_code, plan, insights, notes -> code"
                )
                
            def forward(self, dataset_code, plan, insights, notes):
                return self.generator(
                    dataset_code=dataset_code,
                    plan=plan,
                    insights=insights,
                    notes=notes
                )
                
        self.code_generator = CodeGenerator()
        
        # Create a metric for code quality
        self.metric = ExperimentQualityMetric()
        
    def initial_solve(self):
        """Generate initial solutions."""
        if self.use_dspy:
            # Use DSPy module
            result = self.code_generator(
                dataset_code=self.dataset_code,
                plan=self.plan,
                insights=self.insights,
                notes=self.notes
            )
            
            # Execute and evaluate the code
            code = result.code
            output, results = self._execute_code(code)
            score = self._evaluate_code(code, results)
            
            self.best_codes.append(([code], score, results))
        else:
            # Original implementation
            # ...
            
    def solve(self):
        """Improve solutions using DSPy optimization if enabled."""
        if self.use_dspy:
            # Create a training set from previous iterations
            trainset = []
            for code_list, score, results in self.best_codes:
                for code in code_list:
                    trainset.append(dspy.Example(
                        dataset_code=self.dataset_code,
                        plan=self.plan,
                        insights=self.insights,
                        notes=self.notes,
                        code=code,
                        results=results,
                        score=score
                    ))
                    
            # Optimize the code generator
            optimizer = MLESolverOptimizer(
                metric=lambda gold, pred: self._evaluate_code(pred.code, self._execute_code(pred.code)[1]),
                max_steps=self.max_steps
            )
            
            optimized_generator = optimizer.compile(
                self.code_generator,
                trainset=trainset
            )
            
            # Generate new code
            result = optimized_generator(
                dataset_code=self.dataset_code,
                plan=self.plan,
                insights=self.insights,
                notes=self.notes
            )
            
            # Execute and evaluate
            code = result.code
            output, results = self._execute_code(code)
            score = self._evaluate_code(code, results)
            
            # Update best codes
            self.best_codes.append(([code], score, results))
            self.best_codes.sort(key=lambda x: x[1], reverse=True)
        else:
            # Original implementation
            # ...
            
    def _execute_code(self, code):
        """Execute code and capture output and results."""
        # Implementation...
        
    def _evaluate_code(self, code, results):
        """Evaluate code quality and results."""
        # Implementation...
```

## Testing Plan

### Unit Tests

1. **DSPy Configuration Tests**:
   - Test model mapping
   - Verify configuration settings
   - Check token tracking compatibility

2. **Agent Module Tests**:
   - Verify that each agent module produces expected outputs
   - Test the integration with legacy code
   - Ensure state management works correctly

3. **Phase Module Tests**:
   - Test each phase module independently
   - Verify optimization workflows
   - Validate metrics for each phase

4. **Integration Tests**:
   - Test the complete workflow with DSPy enabled
   - Compare results with DSPy disabled
   - Verify backward compatibility

### Evaluation Metrics

1. **Performance Metrics**:
   - Quality of literature reviews
   - Coherence of research plans
   - Success rate of experiments
   - Quality of final reports

2. **Efficiency Metrics**:
   - Token usage before and after DSPy
   - Time required for each phase
   - Number of iterations needed per phase

3. **User Experience Metrics**:
   - Human ratings of output quality
   - Usability in co-pilot mode
   - Adaptability to user feedback

## Implementation Schedule

### Week 1: Core Infrastructure
- Implement `dspy_config.py`
- Update `inference.py` with DSPy integration
- Create basic structure for DSPy modules

### Week 2: Agent Modules
- Implement base agent modules
- Create phase-specific modules
- Develop custom metrics for each phase

### Week 3: Agent Classes Update
- Update `base_agent.py`
- Modify each specialized agent class
- Ensure backward compatibility

### Week 4: Workflow Orchestration
- Update `LaboratoryWorkflow` class
- Add optimization capabilities
- Test phase transitions

### Week 5: Custom Optimizers
- Implement `MultiAgentOptimizer`
- Create `MLESolverOptimizer`
- Test optimization workflows

### Week 6: Solver Updates
- Update `mlesolver.py`
- Modify `papersolver.py`
- Integrate with full workflow

### Week 7: Testing & Refinement
- Conduct unit and integration tests
- Measure performance improvements
- Address bugs and edge cases

### Week 8: Documentation & Release
- Update documentation
- Create usage examples
- Prepare for release

## Risks and Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Breaking changes to DSPy API | High | Medium | Keep regular updates, maintain compatibility layer |
| Performance regression | High | Low | Comprehensive testing, A/B comparisons |
| Integration complexity | Medium | High | Incremental approach, maintain fallback code |
| LLM cost increases | Medium | Medium | Optimize token usage, implement caching |
| User adoption barriers | Low | Medium | Clear documentation, maintain backward compatibility |

## Conclusion

The integration of DSPy into AgentLaboratory represents a significant architectural enhancement that will improve agent performance, code maintainability, and system flexibility. By leveraging DSPy's optimization capabilities while maintaining the unique multi-agent collaborative workflow, we can create a more powerful and easier-to-extend research automation platform.

The implementation plan is designed to be incremental, with each phase building on the previous one while maintaining backward compatibility throughout. This ensures that existing functionality will not be disrupted while new capabilities are added.