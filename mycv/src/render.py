# mycv/src/render.py
import os
from fpdf import FPDF

class CVRenderer:
    def __init__(self, cv_data, output_dir="output"):
        self.data = cv_data  # Should be the actual dict from loader
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def render_pdf(self, filename="mycv.pdf"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", "B", 16)

        pdf.multi_cell(0, 10, "Curriculum Vitae")
        pdf.ln(5)

        # Iterate actual sections
        for section, items in self.data.items():
            pdf.set_font("Arial", "B", 14)
            pdf.multi_cell(0, 8, section)
            pdf.ln(2)
            pdf.set_font("Arial", "", 12)

            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict):
                        # Flatten dict to string
                        line = ", ".join(f"{k.capitalize()}: {v}" for k, v in item.items())
                        pdf.multi_cell(0, 8, line)
                    else:
                        pdf.multi_cell(0, 8, str(item))
                    pdf.ln(1)
            else:
                pdf.multi_cell(0, 8, str(items))
            pdf.ln(3)

        output_path = os.path.join(self.output_dir, filename)
        pdf.output(output_path, "F")
        return output_path
