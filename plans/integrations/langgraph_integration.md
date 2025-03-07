# LangGraph Integration Plan for Agent Laboratory

## Overview
- **Name**: LangGraph Integration
- **Purpose**: Enhance workflow visibility, tracking, and debugging of multi-agent research processes
- **Implementation Complexity**: Medium - Implementing as an overlay without disrupting core functionality
- **Timeline**: 3 weeks
- **Business Value**: High - Improved visualization, better checkpointing, and enhanced debugging capabilities

## Integration Approach
The integration strategy focuses on implementing LangGraph as a non-invasive overlay that enhances the existing workflow system without requiring a complete rewrite of the agent infrastructure. This approach prioritizes:

1. **Minimal Code Changes**: Wrap existing functionality in LangGraph nodes
2. **Incremental Adoption**: Enable LangGraph features on a per-phase basis
3. **Parallel Implementations**: Allow both original and LangGraph-enhanced workflows
4. **Visualization Benefits**: Add tracing and monitoring without changing core functionality

## Implementation Details

### 1. Project Structure
```
langgraph_integration/
├── __init__.py                    # Package initialization
├── state.py                       # State schema definitions
├── nodes/                         # LangGraph node implementations
│   ├── __init__.py
│   ├── literature_review.py       # Literature review node
│   ├── plan_formulation.py        # Plan formulation node
│   ├── data_preparation.py        # Data preparation node
│   ├── experimentation.py         # Running experiments node
│   ├── interpretation.py          # Results interpretation node
│   ├── report_writing.py          # Report writing node
│   └── refinement.py              # Report refinement node
├── workflows/                     # Workflow graph definitions
│   ├── __init__.py
│   ├── full_research.py           # Complete research workflow
│   └── custom_workflows.py        # User-configurable workflows
├── visualizers/                   # Visualization utilities
│   ├── __init__.py
│   ├── console_tracer.py          # Terminal-based workflow tracing
│   └── web_visualizer.py          # Optional web-based visualization
└── checkpointing/                 # Enhanced state persistence
    ├── __init__.py
    └── memory_manager.py          # State persistence adapter
```

### 2. State Schema Definition

```python
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from langgraph.graph import MessagesState


class AgentLabResearchState(BaseModel):
    """State schema for Agent Laboratory research workflow."""
    
    # Core workflow state
    messages: List[Dict[str, Any]] = Field(default_factory=list)
    phase: str = "init"
    research_topic: str = ""
    
    # Agent outputs by phase
    literature_review: Optional[str] = None
    plan: Optional[str] = None
    dataset_code: Optional[str] = None
    results_code: Optional[str] = None
    exp_results: Optional[str] = None
    interpretation: Optional[str] = None
    report: Optional[str] = None
    
    # Metadata
    phase_statistics: Dict[str, Dict[str, float]] = Field(default_factory=dict)
    reference_papers: List[str] = Field(default_factory=list)
    human_feedback: Dict[str, str] = Field(default_factory=dict)
    
    class Config:
        """Configuration for the state schema."""
        arbitrary_types_allowed = True
```

### 3. Node Implementations

Each node in the LangGraph workflow will wrap existing AgentLaboratory functionality:

```python
from typing import Dict, Any

def literature_review_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Literature review phase node implementation."""
    # Extract research topic from state
    research_topic = state.get("research_topic", "")
    
    # Initialize laboratory workflow with appropriate agents
    from agents import PhDStudentAgent
    phd = PhDStudentAgent(model=state.get("model_backbone"), 
                         notes=state.get("notes", []), 
                         max_steps=state.get("max_steps", 100))
    
    # Run literature review phase
    # This internally utilizes the existing workflow logic
    literature_review_result, statistics = run_literature_review(
        phd, 
        research_topic,
        max_steps=state.get("max_steps", 100),
        arxiv_num_summaries=state.get("arxiv_num_summaries", 5)
    )
    
    # Update state with results
    return {
        "literature_review": literature_review_result,
        "phase": "plan_formulation",
        "phase_statistics": {
            **state.get("phase_statistics", {}),
            "literature_review": statistics
        }
    }
```

### 4. Graph Construction

```python
from langgraph.graph import StateGraph, START, END
import langgraph_integration.nodes as nodes

def create_research_workflow(checkpoint_dir: str = "state_saves/langgraph"):
    """Create a LangGraph workflow for the Agent Laboratory research process."""
    
    # Initialize the state graph
    workflow = StateGraph(AgentLabResearchState)
    
    # Add nodes for each research phase
    workflow.add_node("literature_review", nodes.literature_review_node)
    workflow.add_node("plan_formulation", nodes.plan_formulation_node)
    workflow.add_node("data_preparation", nodes.data_preparation_node)
    workflow.add_node("experimentation", nodes.experimentation_node)
    workflow.add_node("interpretation", nodes.interpretation_node)
    workflow.add_node("report_writing", nodes.report_writing_node)
    workflow.add_node("refinement", nodes.refinement_node)
    workflow.add_node("human_feedback", nodes.human_feedback_node)
    
    # Add edges defining the research workflow
    workflow.add_edge(START, "literature_review")
    workflow.add_edge("literature_review", "plan_formulation")
    workflow.add_edge("plan_formulation", "data_preparation")
    workflow.add_edge("data_preparation", "experimentation")
    workflow.add_edge("experimentation", "interpretation")
    workflow.add_edge("interpretation", "report_writing")
    workflow.add_edge("report_writing", "refinement")
    
    # Add conditional branching for human-in-the-loop and refinement decisions
    workflow.add_conditional_edges(
        "refinement",
        lambda state: "plan_formulation" if state.get("refinement_decision") == "revise" else END
    )
    
    # Add human feedback conditional edges if copilot mode enabled
    workflow.add_conditional_edges(
        "human_feedback",
        lambda state: state.get("next_node", "literature_review")
    )
    
    # Configure checkpointing to enable state persistence
    from langgraph.checkpoint.sqlite import SqliteSaver
    checkpointer = SqliteSaver(f"{checkpoint_dir}/research_workflow.sqlite")
    
    # Compile workflow into a runnable
    return workflow.compile(checkpointer=checkpointer)
```

### 5. Adapter for Existing Codebase

```python
class LangGraphLaboratoryAdapter:
    """
    Adapter to provide LangGraph-based workflow while maintaining
    compatibility with the original LaboratoryWorkflow interface.
    """
    
    def __init__(self, research_topic, openai_api_key, **kwargs):
        """Initialize with same parameters as LaboratoryWorkflow."""
        self.research_topic = research_topic
        self.openai_api_key = openai_api_key
        self.kwargs = kwargs
        
        # Initialize LangGraph workflow
        self.workflow = create_research_workflow()
        
        # Initialize state
        self.initial_state = {
            "research_topic": research_topic,
            "model_backbone": kwargs.get("agent_model_backbone", "o1-mini"),
            "notes": kwargs.get("notes", []),
            "max_steps": kwargs.get("max_steps", 100),
            "human_in_loop_flag": kwargs.get("human_in_loop_flag", {}),
            # Additional configuration parameters
        }
        
    def perform_research(self):
        """
        Execute the LangGraph-based research workflow.
        This maintains the same interface as the original LaboratoryWorkflow.
        """
        # Run the workflow with the initial state
        final_state = self.workflow.invoke(self.initial_state)
        
        # Extract results for compatibility with original interface
        self.phase_status = {
            phase: phase in final_state.get("completed_phases", [])
            for phase in ["literature_review", "plan_formulation", 
                       "data_preparation", "running_experiments",
                       "results_interpretation", "report_writing", 
                       "report_refinement"]
        }
        
        self.statistics_per_phase = final_state.get("phase_statistics", {})
        
        # Return final state for advanced users
        return final_state
```

## Integration Steps

### Phase 1: Core Infrastructure (1 week)
1. Implement state schema and basic graph structure
2. Create node wrappers for existing phase implementations
3. Develop checkpointing and state persistence mechanisms
4. Implement adapter interface for backward compatibility

### Phase 2: Enhanced Visualization (1 week)
1. Implement console-based tracing and visualization
2. Create detailed step-by-step progress tracking
3. Add human feedback integration with visualization
4. Capture and visualize agent interactions

### Phase 3: Testing and Optimization (1 week)
1. Write unit tests for LangGraph integration
2. Develop integration tests with full workflow execution
3. Benchmark performance comparison with original workflow
4. Optimize state management and checkpointing

## Minimal Changes Required

To support this integration, the following changes to the existing codebase are required:

1. **ai_lab_repo.py**: Add LangGraph option
```python
# Add to argument parser
parser.add_argument(
    '--use-langgraph',
    type=str,
    default="False",
    help='Use LangGraph for enhanced workflow visualization and checkpointing.'
)

# Add to main execution logic
if args.use_langgraph.lower() == "true":
    from langgraph_integration import LangGraphLaboratoryAdapter
    lab = LangGraphLaboratoryAdapter(
        research_topic=research_topic,
        notes=task_notes_LLM,
        agent_model_backbone=agent_models,
        human_in_loop_flag=human_in_loop,
        openai_api_key=api_key,
        compile_pdf=compile_pdf,
        num_papers_lit_review=num_papers_lit_review,
        papersolver_max_steps=papersolver_max_steps,
        mlesolver_max_steps=mlesolver_max_steps,
    )
else:
    lab = LaboratoryWorkflow(
        # existing parameters
    )
```

2. **requirements.txt**: Add LangGraph dependency
```
langgraph>=0.0.19
```

3. **laboratory_workflow**: Expose phase methods for external use
   - Add entry points for each phase that can be called externally
   - Ensure agent state management is consistent

## Benefits and Impact
- **Improved Visibility**: Trace and visualize multi-agent research workflows
- **Enhanced Debugging**: Better monitoring of agent states and transitions
- **Robust Checkpointing**: More reliable state persistence and resumption
- **Better Human-in-the-Loop**: Structured points for human intervention
- **Performance Insights**: Identify bottlenecks in the research process
- **Extensibility**: Easier to add new phases or custom workflows
- **Architecture Modernization**: Transition to a more modular, graph-based architecture

## Testing Strategy
- **Unit Tests**: Test each node implementation and state transitions
- **Integration Tests**: Test full workflow execution and state persistence
- **Comparison Tests**: Validate that results match original implementation
- **Performance Tests**: Measure overhead of LangGraph integration
- **User Experience Tests**: Evaluate visualization and debugging improvements

## Rollout Strategy
1. **Developer Preview**: Initial release for testing and feedback
2. **Optional Feature**: Make available as optional feature via flag
3. **Documentation**: Create documentation showcasing visualization benefits
4. **Gradual Adoption**: Allow per-phase adoption of LangGraph features
5. **Full Integration**: Eventually make default workflow system

## Future Extensions
- **Web-Based Visualization**: Add web UI for workflow inspection
- **Time Travel Debugging**: Review and modify past agent decisions
- **Custom Workflow Builder**: Allow researchers to define custom workflows
- **Parallel Agent Execution**: Run independent nodes concurrently
- **Dynamic Node Selection**: Allow runtime selection of agent models per node

## Resources Required
- **Dependencies**: LangGraph, Pydantic
- **Development Time**: 3 weeks for minimal implementation
- **Testing Time**: 1 week for comprehensive testing
- **Documentation**: 2-3 days for user documentation