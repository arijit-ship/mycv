import yaml
import jsonschema

class CVLoader:
    def __init__(self, yaml_path, schema_path):
        self.yaml_path = yaml_path
        self.schema_path = schema_path
        self.data = None
        self.schema = None

    def load_schema(self):
        """Loads the validation schema from a YAML file."""
        try:
            with open(self.schema_path, 'r') as f:
                self.schema = yaml.safe_load(f)
            print("✅ Schema loaded successfully.")
        except FileNotFoundError:
            print(f"❌ Error: Schema file not found at {self.schema_path}")
            exit(1)

    def load_data(self):
        """Loads the CV data from a YAML file."""
        try:
            with open(self.yaml_path, 'r') as f:
                self.data = yaml.safe_load(f)
            print("✅ Data loaded successfully.")
        except FileNotFoundError:
            print(f"❌ Error: CV data file not found at {self.yaml_path}")
            exit(1)
            
    def validate_data(self):
        """Validates the loaded data against the schema."""
        if not self.data or not self.schema:
            print("⚠️ Data or schema not loaded. Aborting validation.")
            return False
            
        try:
            jsonschema.validate(instance=self.data, schema=self.schema)
            print("✅ Data validated successfully.")
            return True
        except jsonschema.exceptions.ValidationError as e:
            print("❌ Validation Error:")
            print(e)
            return False

    def get_data(self):
        """Returns the validated data."""
        return self.data