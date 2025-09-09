import argparse
from src.loader import CVLoader
from src.render import CVRenderer

class MyCV:
    def __init__(self, data_file, theme="classic"):
        self.loader = CVLoader(data_file, "mycv/settings/schema.yml")
        self.renderer = CVRenderer(theme)

    def generate_tex(self, output_file="output.tex"):
        tex_path = self.renderer.render_to_tex(self.loader.data["cv"], output_file)
        print(f"LaTeX source generated: {tex_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flexible CV LaTeX Generator")
    parser.add_argument("--yaml", required=True, help="Path to CV YAML file")
    parser.add_argument("--theme", default="classic", help="Theme to use")
    args = parser.parse_args()

    cv = MyCV(args.yaml, args.theme)
    cv.generate_tex()
