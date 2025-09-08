import os
from pathlib import Path
from src.loader import CVLoader
from src.render import CVRenderer
import configparser

class MyCV:
    """
    Main CV object.
    Loads data using CVLoader and provides access to all sections.
    Can also render CV using templates.
    """

    def __init__(self, data_file="mycv.yaml", config_file="settings/config.ini"):
        # -------------------------
        # Load configuration
        # -------------------------
        self.config_file = Path(config_file)
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)

        # Output directory from config
        self.output_dir = Path(self.config.get("general", "output_dir", fallback="output"))
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Default theme
        self.default_theme = self.config.get("general", "default_theme", fallback="classic")

        # -------------------------
        # Load CV data
        # -------------------------
        if not os.path.exists(data_file):
            raise FileNotFoundError(f"{data_file} not found.")
        self.loader = CVLoader(data_file)
        self.loader.load()  # Populate cv_data

    # -------------------------
    # Expose loader methods
    # -------------------------
    @property
    def personal_info(self):
        return self.loader.get_personal_info()

    @property
    def about(self):
        return self.loader.get_about()

    @property
    def education(self):
        return self.loader.get_education()

    @property
    def experience(self):
        return self.loader.get_experience()

    @property
    def skills(self):
        return self.loader.get_skills()

    @property
    def projects(self):
        return self.loader.get_projects()

    @property
    def certificates(self):
        return self.loader.get_certificates()

    @property
    def presentations(self):
        return self.loader.get_presentations()

    def get_section(self, key):
        return self.loader.get_section(key)

    # -------------------------
    # Rendering methods
    # -------------------------
    def render(self, theme=None, output_name="mycv_output"):
        """
        Render CV using the specified theme.
        :param theme: theme folder name (default from config)
        :param output_name: base name for output file
        :return: Path to rendered file
        """
        if theme is None:
            theme = self.default_theme

        template_file = Path(f"themes/{theme}/{theme}.tex")
        if not template_file.exists():
            raise FileNotFoundError(f"Template '{template_file}' not found for theme '{theme}'.")

        renderer = CVRenderer(cv_data=self.loader.cv_data, template_path=template_file, output_dir=self.output_dir)
        rendered_file = renderer.render(output_name)
        return rendered_file

    def compile_pdf(self, rendered_file):
        """
        Compile the rendered file to PDF (if supported).
        :param rendered_file: Path to the rendered file
        :return: Path to PDF file or None
        """
        renderer = CVRenderer(cv_data=self.loader.cv_data, template_path=rendered_file, output_dir=self.output_dir)
        return renderer.compile_pdf(rendered_file)


# -------------------------------
# Example usage
# -------------------------------
if __name__ == "__main__":
    cv = MyCV("mycv.yaml")
    print("Name:", cv.personal_info.get("name"))
    print("Education:", cv.education)
    print("Projects:", cv.projects)

    # Render with default theme
    rendered_file = cv.render()
    print("Rendered file saved at:", rendered_file)

    # Compile to PDF
    pdf_file = cv.compile_pdf(rendered_file)
    print("PDF file saved at:", pdf_file)
