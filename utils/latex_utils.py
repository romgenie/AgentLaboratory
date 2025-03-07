import os
import subprocess
import re

def compile_latex(latex_code, compile=True, output_filename="output.pdf", timeout=30):
    """
    Compile LaTeX code into a PDF document.
    
    Args:
        latex_code (str): The LaTeX code to compile
        compile (bool): Whether to actually compile the code or just prepare it
        output_filename (str): The name of the output PDF file
        timeout (int): Maximum time in seconds for compilation
        
    Returns:
        str: Compilation result message
    """
    latex_code = latex_code.replace(
        r"\documentclass{article}",
        "\\documentclass{article}\n\\usepackage{amsmath}\n\\usepackage{amssymb}\n\\usepackage{array}\n\\usepackage{algorithm}\n\\usepackage{algorithmicx}\n\\usepackage{algpseudocode}\n\\usepackage{booktabs}\n\\usepackage{colortbl}\n\\usepackage{color}\n\\usepackage{enumitem}\n\\usepackage{fontawesome5}\n\\usepackage{float}\n\\usepackage{graphicx}\n\\usepackage{hyperref}\n\\usepackage{listings}\n\\usepackage{makecell}\n\\usepackage{multicol}\n\\usepackage{multirow}\n\\usepackage{pgffor}\n\\usepackage{pifont}\n\\usepackage{soul}\n\\usepackage{sidecap}\n\\usepackage{subcaption}\n\\usepackage{titletoc}\n\\usepackage[symbol]{footmisc}\n\\usepackage{url}\n\\usepackage{wrapfig}\n\\usepackage{xcolor}\n\\usepackage{xspace}")
    
    dir_path = "research_dir/tex"
    # Create the directory if it doesn't exist
    os.makedirs(dir_path, exist_ok=True)
    tex_file_path = os.path.join(dir_path, "temp.tex")
    
    # Write the LaTeX code to the .tex file in the specified directory
    with open(tex_file_path, "w") as f:
        f.write(latex_code)

    if not compile:
        return f"Compilation successful"

    # Compiling the LaTeX code using pdflatex with non-interactive mode and timeout
    try:
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "temp.tex"],
            check=True,                   # Raises a CalledProcessError on non-zero exit codes
            stdout=subprocess.PIPE,        # Capture standard output
            stderr=subprocess.PIPE,        # Capture standard error
            timeout=timeout,               # Timeout for the process
            cwd=dir_path
        )

        # If compilation is successful, return the success message
        return f"Compilation successful: {result.stdout.decode('utf-8')}"

    except subprocess.TimeoutExpired:
        # If the compilation takes too long, return a timeout message
        return "[CODE EXECUTION ERROR]: Compilation timed out after {} seconds".format(timeout)
    except subprocess.CalledProcessError as e:
        # If there is an error during LaTeX compilation, return the error message
        return f"[CODE EXECUTION ERROR]: Compilation failed: {e.stderr.decode('utf-8')} {e.output.decode('utf-8')}. There was an error in your latex."
    
def escape_latex_special_chars(text):
    """
    Escape special LaTeX characters in a string.
    
    Args:
        text (str): The input text to escape
        
    Returns:
        str: The escaped text ready for inclusion in LaTeX documents
    """
    # Define LaTeX special characters and their escaped versions
    special_chars = {
        '&': r'\&', 
        '%': r'\%', 
        '$': r'\$', 
        '#': r'\#', 
        '_': r'\_', 
        '{': r'\{', 
        '}': r'\}', 
        '~': r'\textasciitilde{}', 
        '^': r'\textasciicircum{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless{}',
        '>': r'\textgreater{}'
    }
    
    # Replace each special character with its escaped version
    for char, replacement in special_chars.items():
        text = text.replace(char, replacement)
        
    return text

def verify_latex_compilation(latex_code):
    """
    Verify if a LaTeX document can be compiled without actually producing output.
    
    Args:
        latex_code (str): The LaTeX code to verify
        
    Returns:
        tuple: (bool, str) indicating success and error message if any
    """
    dir_path = "research_dir/tex"
    # Create the directory if it doesn't exist
    os.makedirs(dir_path, exist_ok=True)
    tex_file_path = os.path.join(dir_path, "verify.tex")
    
    # Write the LaTeX code to a temporary file
    with open(tex_file_path, "w") as f:
        f.write(latex_code)
    
    try:
        # Use -draftmode to skip producing output files
        result = subprocess.run(
            ["pdflatex", "-draftmode", "-interaction=nonstopmode", "verify.tex"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
            cwd=dir_path
        )
        return True, "Verification successful"
    except subprocess.CalledProcessError as e:
        return False, f"Verification failed: {e.stderr.decode('utf-8') if e.stderr else e.stdout.decode('utf-8')}"
    except subprocess.TimeoutExpired:
        return False, "Verification timed out"
    except Exception as e:
        return False, f"Error during verification: {str(e)}"
    finally:
        # Clean up temporary files
        try:
            os.remove(tex_file_path)
            # Remove auxiliary files
            for ext in ['.aux', '.log', '.out']:
                aux_file = os.path.join(dir_path, f"verify{ext}")
                if os.path.exists(aux_file):
                    os.remove(aux_file)
        except:
            pass