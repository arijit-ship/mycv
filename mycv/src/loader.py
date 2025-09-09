import yaml
import os

class CVLoader:
    def __init__(self, data_file, schema_file):
        self.data_file = data_file
        self.schema_file = schema_file
        self.data = None
        self.schema = None
        self._load_data()

    def _load_data(self):
        if not os.path.exists(self.data_file):
            raise FileNotFoundError(f"YAML file not found: {self.data_file}")
        if not os.path.exists(self.schema_file):
            raise FileNotFoundError(f"Schema file not found: {self.schema_file}")

        with open(self.schema_file, 'r', encoding='utf-8') as f:
            self.schema = yaml.safe_load(f)

        with open(self.data_file, 'r', encoding='utf-8') as f:
            self.data = yaml.safe_load(f)

        self._validate_cv(self.data['cv'])

    def _validate_cv(self, cv_sections):
        for section in cv_sections:
            heading = section.get('heading')
            contents = section.get('contents', [])
            if heading in self.schema:
                allowed_keys = self.schema[heading]
                for item in contents:
                    self._validate_item(item, allowed_keys)
            else:
                # Allow custom sections without validation
                continue

    def _validate_item(self, item, allowed_keys):
        for key, value in item.items():
            if key not in allowed_keys:
                raise ValueError(f"Invalid key '{key}' in section '{key}'. Allowed keys: {list(allowed_keys.keys())}")
            if isinstance(value, dict) and isinstance(allowed_keys[key], dict):
                self._validate_item(value, allowed_keys[key])
            elif isinstance(value, list) and isinstance(allowed_keys[key], list):
                for elem in value:
                    if isinstance(elem, dict) and isinstance(allowed_keys[key][0], dict):
                        self._validate_item(elem, allowed_keys[key][0])
