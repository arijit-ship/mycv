import os
import yaml
from cerberus import Validator


class CVLoader:
    def __init__(self, data_file, schema_file):
        self.data_file = data_file
        self.schema_file = schema_file
        self.data = None
        self.schema = None
        self._load_schema()
        self._load_data()

    def _load_schema(self):
        """Load YAML schema definition."""
        if not os.path.exists(self.schema_file):
            raise FileNotFoundError(f"Schema file {self.schema_file} not found.")
        with open(self.schema_file, "r", encoding="utf-8") as f:
            self.schema = yaml.safe_load(f)

    def _load_data(self):
        """Load CV YAML data and validate."""
        if not os.path.exists(self.data_file):
            raise FileNotFoundError(f"Data file {self.data_file} not found.")
        with open(self.data_file, "r", encoding="utf-8") as f:
            self.data = yaml.safe_load(f)

        self._validate_data()

    def _validate_data(self):
        """Validate CV data against schema using Cerberus."""
        v = Validator(self.schema)
        v.allow_unknown = True  # allow arbitrary fields in contents
        if not v.validate(self.data):
            raise ValueError(f"Invalid CV data: {v.errors}")

    def get_sections(self):
        """Return the list of sections."""
        return self.data.get("cv", {}).get("sections", [])
