from jinja2 import Environment, FileSystemLoader
import subprocess
import os

class CVRenderer:
    def __init__(self, template_path, output_path):
        self.template_path = template_path
        self.output_path = output_path
        # Set up Jinja2 environment with the parent directory of the template
        template_dir = os.path.dirname(template_path)
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            block_start_string='((%',
            block_end_string='%))',
            variable_start_string='(((',
            variable_end_string=')))',
            comment_start_string='((#',
            comment_end_string='#))'
        )
        self.template_file = os.path.basename(template_path)

    def render_latex(self, data):
        """Renders the Jinja2 template with the provided data."""
        template = self.env.get_template(self.template_file)
        rendered_content = template.render(data)
        
        latex_file = os.path.join(self.output_path, 'mycv.tex')
        with open(latex_file, 'w') as f:
            f.write(rendered_content)
        print(f"✅ LaTeX file '{latex_file}' generated.")
        return latex_file

    def compile_pdf(self, latex_file):
        """Compiles the LaTeX file into a PDF using pdflatex."""
        try:
            # Change to the output directory for compilation
            cwd = os.getcwd()
            os.chdir(self.output_path)
            
            # Run pdflatex command
            subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", os.path.basename(latex_file)],
                check=True,
                capture_output=True,
                text=True
            )
            print("✅ PDF compiled successfully.")
            
            # Clean up auxiliary files
            for ext in ['.aux', '.log', '.out']:
                file_to_remove = os.path.basename(latex_file).replace('.tex', ext)
                if os.path.exists(file_to_remove):
                    os.remove(file_to_remove)
            print("✅ Auxiliary files cleaned up.")

            # Return to the original working directory
            os.chdir(cwd)
            
        except subprocess.CalledProcessError as e:
            print("❌ LaTeX compilation failed.")
            print("--- Compiler Output ---")
            print(e.stdout)
            print("--- Compiler Errors ---")
            print(e.stderr)
            exit(1)
        except FileNotFoundError:
            print("❌ Error: 'pdflatex' command not found. Please ensure LaTeX is installed and in your system's PATH.")
            exit(1)