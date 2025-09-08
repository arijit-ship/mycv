import os
from jinja2 import Environment, FileSystemLoader
import subprocess
from pathlib import Path

class CVRenderer:
    """
    Flexible CV Renderer using Jinja2 templates.
    Supports multiple formats: LaTeX, HTML, Markdown, Word (docx), and plain text.
    """

    def __init__(self, cv_data, template_path, output_dir="output"):
        """
        :param cv_data: dict, CV data loaded from YAML/JSON
        :param template_path: str or Path, path to the template file
        :param output_dir: str, folder to save rendered files
        """
        self.cv_data = cv_data
        self.template_path = Path(template_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        if not self.template_path.exists():
            raise FileNotFoundError(f"Template '{template_path}' not found.")

        # Determine file type from extension
        self.file_type = self.template_path.suffix.lower()

    def render(self, output_name="cv"):
        """
        Render the template with CV data.
        :param output_name: base name for output file (without extension)
        :return: path to rendered file
        """
        env = Environment(
            loader=FileSystemLoader(str(self.template_path.parent)),
            autoescape=False
        )
        template = env.get_template(self.template_path.name)
        rendered_content = template.render(cv=self.cv_data)

        # Determine output file based on template type
        output_file = self.output_dir / f"{output_name}{self.template_path.suffix.lower()}"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(rendered_content)

        return output_file

    def compile_pdf(self, rendered_file):
        """
        Compile rendered file into PDF (only LaTeX or HTML currently supported).
        :param rendered_file: Path or str to the rendered file
        :return: Path to PDF file or None if failed/unsupported
        """
        rendered_file = Path(rendered_file)
        pdf_file = self.output_dir / f"{rendered_file.stem}.pdf"

        if rendered_file.suffix.lower() == ".tex":
            try:
                subprocess.run(
                    ["pdflatex", "-interaction=nonstopmode", "-output-directory", str(self.output_dir), str(rendered_file)],
                    check=True
                )
                return pdf_file
            except subprocess.CalledProcessError:
                raise RuntimeError("LaTeX compilation failed. Check your template and LaTeX installation.")

        elif rendered_file.suffix.lower() == ".html":
            try:
                import pdfkit
                pdfkit.from_file(str(rendered_file), str(pdf_file))
                return pdf_file
            except ImportError:
                raise ImportError("pdfkit not installed. Install via 'pip install pdfkit' and wkhtmltopdf.")
        else:
            raise NotImplementedError(f"PDF compilation not supported for '{rendered_file.suffix}' yet.")
