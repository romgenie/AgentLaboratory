from mlsolver.command import Command


class Replace(Command):
    """Command implementation for replacing entire code."""
    
    def __init__(self):
        super().__init__()
        self.cmd_type = "CODE-replace"

    def docstring(self) -> str:
        return (
            "============= REWRITE CODE EDITING TOOL =============\n"
            "You also have access to a code replacing tool. \n"
            "This tool allows you to entirely re-write/replace all of the current code and erase all existing code.\n"
            "You can use this tool via the following command: ```REPLACE\n<code here>\n```, where REPLACE is the word REPLACE and <code here> will be the new code that is replacing the entire set of old code. This tool is useful if you want to make very significant changes, such as entirely changing the model, or the learning process. Before changing the existing code to be your new code, your new code will be tested and if it returns an error it will not replace the existing code. Try limiting the use of rewriting and aim for editing the code more."
        )

    def execute_command(self, *args) -> str:
        # args[0] -> new code
        args = args[0]
        return args[0]

    def matches_command(self, cmd_str) -> bool:
        if "```REPLACE" in cmd_str: 
            return True
        return False

    def parse_command(self, *args) -> tuple:
        from mlesolver import extract_prompt, execute_code
        
        new_code = extract_prompt(args[0], "REPLACE")
        code_exec = f"{args[1]}\n{new_code}"
        code_ret = execute_code(code_exec)
        if "[CODE EXECUTION ERROR]" in code_ret: 
            return False, (None, code_ret,)
        return True, (new_code.split("\n"), code_ret)
