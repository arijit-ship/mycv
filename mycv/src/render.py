import os
from jinja2 import Environment, FileSystemLoader
import subprocess

class CVRenderer:
    def __init__(self, theme="classic", output_dir="output"):
        self.theme = theme
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

        self.template_dir = os.path.join(
            os.path.dirname(__file__), "../themes", theme
        )
        self.env = Environment(loader=FileSystemLoader(self.template_dir))

    # -----------------------------
    # LaTeX escaping
    # -----------------------------
    def escape_latex(self, text):
        """Escape LaTeX special characters"""
        if not isinstance(text, str):
            return text
        replacements = {
            "&": r"\&",
            "%": r"\%",
            "$": r"\$",
            "#": r"\#",
            "_": r"\_",
            "{": r"\{",
            "}": r"\}",
            "~": r"\textasciitilde{}",
            "^": r"\textasciicircum{}",
            "\\": r"\textbackslash{}",
        }
        for char, repl in replacements.items():
            text = text.replace(char, repl)
        return text

    # -----------------------------
    # Render TEX
    # -----------------------------
    def render_to_tex(self, cv_data, output_file="output.tex"):
        template = self.env.get_template("classic.tex.j2")
        rendered = template.render(cv=cv_data, escape_latex=self.escape_latex)

        output_path = os.path.join(self.output_dir, output_file)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(rendered)
        return output_path

    # -----------------------------
    # Compile PDF
    # -----------------------------
    def tex_to_pdf(self, tex_file, pdf_file="output.pdf"):
        # Compile using pdflatex
        subprocess.run(["pdflatex", "-interaction=nonstopmode", tex_file], check=True)

        # Move PDF to output folder
        basename = os.path.splitext(tex_file)[0]
        pdf_path = os.path.join(self.output_dir, pdf_file)
        if os.path.exists(basename + ".pdf"):
            os.rename(basename + ".pdf", pdf_path)
        return pdf_path

    # -----------------------------
    # Render plain text
    # -----------------------------
    def render_to_text(self, cv_data, output_file="cv.txt"):
        lines = []
        for section in cv_data:
            heading = section.get("heading", "").upper()
            lines.append(heading)
            lines.append("-" * len(heading))

            for item in section.get("contents", []):
                lines.extend(self._render_item_text(item, indent=2))
            lines.append("")

        output_path = os.path.join(self.output_dir, output_file)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return output_path

    def _render_item_text(self, item, indent=0):
        """Recursive helper to render dict/list as text"""
        lines = []
        prefix = " " * indent
        if isinstance(item, dict):
            for key, value in item.items():
                if isinstance(value, dict):
                    lines.append(f"{prefix}{key}:")
                    lines.extend(self._render_item_text(value, indent + 2))
                elif isinstance(value, list):
                    lines.append(f"{prefix}{key}:")
                    for elem in value:
                        lines.extend(self._render_item_text(elem, indent + 2))
                else:
                    lines.append(f"{prefix}{key}: {value}")
        else:
            lines.append(f"{prefix}- {item}")
        return lines
