from copy import copy
import random


class MLESolver:
    """Machine Learning Engineer Solver class for automated ML solution generation."""
    
    def __init__(self, dataset_code, openai_api_key=None, notes=None, max_steps=10, 
                 insights=None, plan=None, llm_str=None):
        if notes is None: 
            self.notes = []
        else: 
            self.notes = notes
        
        self.dataset_code = dataset_code
        
        if plan is None: 
            self.plan = ""
        else: 
            self.plan = plan
            
        self.llm_str = llm_str
        self.verbose = False
        self.max_codes = 2
        self.st_hist_len = 2
        self.min_gen_trials = 2
        self.code_lines = str()
        self.st_history = list()
        self.insights = insights
        self.code_reflect = str()
        self.max_steps = max_steps
        self.prev_code_ret = str()
        self.should_execute_code = True
        self.openai_api_key = openai_api_key
        self.commands = []

    def system_prompt(self, commands=True):
        """
        Produce a system prompt for the mle-solver to solve ml problems
        @param commands: (bool) whether to use command prompt
        @return: (str) system prompt
        """
        return (
            # ROLE DESCRIPTION
            f"{self.role_description()}.\n"
            # TASK INSTRUCTIONS
            f"The following are your task instructions: {self.phase_prompt()}\n"
            # LIT REVIEW INSIGHTS
            f"Provided below are some insights from a literature review summary:\n{self.insights}\n"
            # CODE INSIGHTS
            f"{self.code_reflect}"
            # NOTES
            f"The following are notes, instructions, and general tips for you: {self.notes}"
            # PLAN DESCRIPTION
            f"You are given a machine learning research task described, where the plan is described as follows: {self.plan}\n"
            # DATASET DESCRIPTION            
            f"{self.generate_dataset_descr_prompt()}"
            # Create Figures
            f"You should also try generating at least two figures to showcase the results, titled Figure_1.png and Figure_2.png\n"
            f"Your method MUST not get 0% accuracy. If it does, you have done something wrong and must correct this. Make sure to check your accuracy calculation is correct.\n"
            # transition
            f"Your goal is to solve the research plan as well as possible. You will receive a score after you write the code and should aim to maximize the score by following the plan instructions and writing high quality code.\n"
            f"Before each experiment please include a print statement explaining exactly what the results are meant to show in great detail before printing the results out.\n"
            # COMMAND SET
            f"The following are commands you have access to: {self.command_descriptions()}\n. You should try to have a diversity of command responses if appropriate. Do not repeat the same commend too many times. Please consider looking through your history and not repeating commands too many times." if commands else ""
        )
    
    def role_description(self):
        """
        Provide role description
        @return: (str) role description
        """
        return "You are an expert machine learning engineer working at a top university to write code to solve machine learning research challenges using your machine learning expertise."
    
    def phase_prompt(self):
        """
        Describe system role and general tips for mle-solver
        @return: (str) system role
        """
        phase_str = (
            "You are an ML engineer and you will be writing the code for a research project.\n"
            "Your goal is to produce code that obtains final results for a set of research experiments. You should aim for simple code to collect all results, not complex code. You should integrate the provided literature review and the plan to make sure you are implementing everything outlined in the plan. The dataset code will be added to the beginning of your code always, so this does not need to be rewritten. Make sure you do not write functions, only loose code.\n"
            "I would recommend writing smaller code so you do not run out of time but make sure to work on all points in the plan in the same code. You code should run every experiment outlined in the plan for a single code.\n",
            "You cannot pip install new libraries, but many machine learning libraries already work. If you wish to use a language model in your code, please use the following:\nAnything you decide to print inside your code will be provided to you as input, and you will be able to see that part of the code. Using print statements is useful for figuring out what is wrong and understanding your code better."
        )
        return phase_str
    
    def generate_dataset_descr_prompt(self):
        """
        Generate description prompt for dataset
        @return: (str) description prompt
        """
        return f"\n- The following dataset code will be added to the beginning of your code always, so this does not need to be rewritten: {self.dataset_code}"
    
    def command_descriptions(self):
        """
        Provide command descriptions
        @return: (str) command descriptions
        """
        cmd_strings = "\n".join([_cmd.docstring() for _cmd in self.commands])
        return f"\nYou also have access to tools which can be interacted with using the following structure: ```COMMAND\n<command information here>\n```, where COMMAND is whichever command you want to run (e.g. EDIT, REPLACE...), <command information here> is information used for the command, such as code to run or a search query, and ``` are meant to encapsulate the command. ``` must be included as part of the command both at the beginning and at the end of the code. DO NOT FORGOT TO HAVE ``` AT THE TOP AND BOTTOM OF CODE. and this structure must be followed to execute a command correctly. YOU CAN ONLY EXECUTE A SINGLE COMMAND AT A TIME! Do not try to perform multiple commands EVER only one." + cmd_strings
    
    def process_command(self, cmd_str):
        """Process a command string and execute the corresponding command."""
        # Simplified version for testing purposes
        code_lines = []
        prev_code_ret = "Command processed successfully"
        should_execute_code = True
        score = 0.85  # Mock score
        return cmd_str, code_lines, prev_code_ret, should_execute_code, score


def get_score(outlined_plan, code, code_return, REWARD_MODEL_LLM, attempts=3, openai_api_key=None):
    """Calculate a score for the produced code based on how well it follows the plan."""
    # Mock implementation for testing
    return 0.85, "The performance of your submission is: 0.85", True


def code_repair(code, error, ctype, REPAIR_LLM, openai_api_key=None):
    """Repair code based on error messages."""
    # Mock implementation for testing
    if ctype == "replace":
        return "def repaired_function():\n    return 'Fixed code'"
    elif ctype == "edit":
        return "```EDIT 1 2\ndef fixed_function():\n    return 'Fixed code'\n```"
    return code


def execute_code(code_str):
    """Execute the given code string and return the result."""
    # Mock implementation for testing
    return "Code executed successfully with result: 42"


def extract_prompt(text, word):
    """Extract content between markers in a prompt."""
    # Mock implementation for testing
    if word == "REPLACE":
        return "def extracted_code():\n    return 'Extracted code'"
    elif word == "EDIT":
        return "1 2\ndef edited_code():\n    return 'Edited code'"
    return text
