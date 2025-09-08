# mycv/src/loader.py

import yaml
import json
import os
from cerberus import Validator

class CVLoader:
    """
    Dynamic CV Loader
    - Loads YAML or JSON CV files
    - Validates against a schema
    - Provides dynamic access to sections and keys
    """

    def __init__(self, data_file, schema_file="mycv/settings/schema.yaml"):
        if not os.path.exists(data_file):
            raise FileNotFoundError(f"CV data file {data_file} not found.")
        if not os.path.exists(schema_file):
            raise FileNotFoundError(f"Schema file {schema_file} not found.")
        
        self.data_file = data_file
        self.schema_file = schema_file
        self.cv_data = None
        self.schema = None
        self._load_schema()
        self._load_data()

    def _load_schema(self):
        """Load YAML schema"""
        with open(self.schema_file, "r") as f:
            self.schema = yaml.safe_load(f)

    def _load_data(self):
        """Load YAML or JSON data and validate"""
        ext = os.path.splitext(self.data_file)[1].lower()
        with open(self.data_file, "r") as f:
            if ext in [".yaml", ".yml"]:
                self.cv_data = yaml.safe_load(f)
            elif ext == ".json":
                self.cv_data = json.load(f)
            else:
                raise ValueError("Unsupported file format. Use YAML or JSON.")

        self._validate_data()

    def _validate_data(self):
        """Validate the loaded CV against schema"""
        v = Validator(self.schema, allow_unknown=True)
        if not v.validate(self.cv_data):
            raise ValueError(f"CV data validation failed: {v.errors}")

    # ---------------------------
    # Dynamic access methods
    # ---------------------------
    def get_sections(self):
        """Return all top-level section keys"""
        return list(self.cv_data.keys())

    def get_section(self, section_key):
        """Return content dict of a section, or None if section not exists"""
        return self.cv_data.get(section_key)

    def get_content(self, section_key, key=None):
        """
        Get content inside a section
        If key is None, return full content dict
        Otherwise return the value for that key (or None if missing)
        """
        section = self.cv_data.get(section_key)
        if not section:
            return None
        content = section.get("content")
        if content is None:
            return None
        if key:
            return content.get(key) if isinstance(content, dict) else None
        return content

    def all_data(self):
        """Return the full loaded CV"""
        return self.cv_data
