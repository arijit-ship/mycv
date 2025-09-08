# mycv/mycv.py
import os
import argparse
from src.loader import CVLoader
from src.render import CVRenderer

class MyCV:
    """
    Main CV object.
    Loads data using CVLoader and provides access to all sections.
    """

    def __init__(self, data_file, schema_file=None):
        if not os.path.exists(data_file):
            raise FileNotFoundError(f"{data_file} not found.")
        if schema_file and not os.path.exists(schema_file):
            raise FileNotFoundError(f"{schema_file} not found.")

        self.loader = CVLoader(data_file, schema_file)
        self.data = self.loader.data

    def display_sections(self):
        """Print all sections with their content."""
        for section, contents in self.data.items():
            print(f"Section: {section}")
            for item in contents:
                print(f"  - {item}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MyCV CLI")
    parser.add_argument("--yaml", type=str, required=True, help="Path to CV YAML file")
    parser.add_argument("--schema", type=str, help="Optional path to schema file")
    parser.add_argument("--to", type=str, default="pdf", choices=["pdf"], help="Output format")
    parser.add_argument("--output", type=str, default="output", help="Output directory")
    args = parser.parse_args()

    # Load CV
    cv = MyCV(data_file=args.yaml, schema_file=args.schema)
    cv.display_sections()

    # Render PDF
    if args.to == "pdf":
        renderer = CVRenderer(cv.data, output_dir=args.output)
        pdf_path = renderer.render_pdf()
        print(f"PDF generated at: {pdf_path}")
