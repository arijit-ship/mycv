import os
from fpdf import FPDF

class CVRenderer:
    def __init__(self, cv_data, output_dir="output"):
        self.data = cv_data
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

        # Path to a Unicode-capable system font
        self.font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        if not os.path.isfile(self.font_path):
            raise FileNotFoundError(
                f"System font not found: {self.font_path}. "
                "Install fonts-dejavu or change font_path."
            )

    def render_pdf(self, filename="mycv.pdf"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Add the font once (regular) with uni=True
        pdf.add_font("DejaVu", "", self.font_path, uni=True)
        pdf.set_font("DejaVu", "", 16)  # Use "" style, not "B"

        pdf.multi_cell(0, 10, "Curriculum Vitae")
        pdf.ln(5)

        for section, items in self.data.items():
            pdf.set_font("DejaVu", "", 14)  # Use regular for headings
            pdf.multi_cell(0, 8, section)
            pdf.ln(2)
            pdf.set_font("DejaVu", "", 12)  # Use regular for body

            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict):
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
