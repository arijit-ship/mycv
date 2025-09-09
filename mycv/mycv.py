import argparse
from src.loader import CVLoader
from src.render import CVRenderer
import os

def main():
    parser = argparse.ArgumentParser(description="A YAML-driven CV/resume generator.")
    parser.add_argument("yaml_file", help="Path to the YAML data file (e.g., mycv.yml).")
    parser.add_argument("--theme", default="classic", help="The name of the theme to use.")
    args = parser.parse_args()

    # Define paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    settings_dir = os.path.join(base_dir, 'settings')
    themes_dir = os.path.join(base_dir, 'themes')
    output_dir = os.path.join(base_dir, 'output') # We'll create a new output directory

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    yaml_path = args.yaml_file
    schema_path = os.path.join(settings_dir, 'schema.yml')
    theme_path = os.path.join(themes_dir, args.theme, f"{args.theme}.tex.j2")

    # Step 1: Load and Validate Data
    loader = CVLoader(yaml_path, schema_path)
    loader.load_schema()
    loader.load_data()

    if not loader.validate_data():
        print("🛑 CV generation aborted due to validation errors.")
        return

    cv_data = loader.get_data()

    # Step 2: Render and Compile
    renderer = CVRenderer(theme_path, output_dir)
    latex_file = renderer.render_latex(cv_data)
    renderer.compile_pdf(latex_file)

    print("🎉 CV generation complete! Check the 'output' directory for your PDF.")

if __name__ == "__main__":
    main()