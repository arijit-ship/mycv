import os
import yaml
import json

class CVLoader:
    """
    A modular CV loader that can parse multiple formats (YAML, JSON, etc.)
    and provides methods to fetch specific sections of the CV.
    """

    # Supported loaders
    _loaders = {
        "yaml": "yaml",
        "yml": "yaml",
        "json": "json"
    }

    def __init__(self, filepath):
        self.filepath = filepath
        self.cv_data = self._load_file()

    def _load_file(self):
        """Detect file type and load data accordingly."""
        ext = os.path.splitext(self.filepath)[1].lower()[1:]
        loader_type = self._loaders.get(ext)

        if loader_type is None:
            raise ValueError(f"Unsupported file format: {ext}")

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                if loader_type == "yaml":
                    return yaml.safe_load(f)
                elif loader_type == "json":
                    return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{self.filepath}' not found.")
        except Exception as e:
            raise ValueError(f"Error reading file: {e}")

    # -------------------------------
    # Section fetchers
    # -------------------------------
    def get_personal_info(self):
        return self.cv_data.get("personal_info", {})

    def get_about(self):
        return self.cv_data.get("about", {})

    def get_education(self):
        return self.cv_data.get("education", [])

    def get_experience(self):
        return self.cv_data.get("experience", [])

    def get_skills(self):
        return self.cv_data.get("skills", {})

    def get_projects(self):
        return self.cv_data.get("projects", [])

    def get_certificates(self):
        return self.cv_data.get("certificates", [])

    def get_presentations(self):
        return self.cv_data.get("presentations", [])

    # General method to fetch any key
    def get_section(self, key):
        return self.cv_data.get(key, None)

