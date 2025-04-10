import requests
import argparse
from fpdf import FPDF

def fetch_resume(name):
    url = f"https://expressjs-api-resume-random.onrender.com/resume?name={name}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            print("Error: Invalid JSON response from API.")
            return None
    else:
        print(f"Error fetching resume. HTTP Status Code: {response.status_code}")
        return None

def create_pdf(resume_data, font_size, font_color, background_color, name):
    pdf = FPDF()
    pdf.add_page()

    # Convert Hex to RGB
    try:
        bg_color = tuple(int(background_color[i:i+2], 16) for i in (1,3,5))
        text_color = tuple(int(font_color[i:i+2], 16) for i in (1,3,5))
    except ValueError:
        print("Error: Invalid color format. Use HEX format like #FFFFFF.")
        return

    pdf.set_fill_color(*bg_color)
    pdf.rect(0, 0, 210, 297, style='F')  # Fixed missing height

    pdf.set_font("Arial", size=font_size)
    pdf.set_text_color(*text_color)

    pdf.cell(200, 10, f"Resume: {name}", ln=True, align='C')

    # Ensure resume_data is a dictionary
    if isinstance(resume_data, dict):
        for key, value in resume_data.items():
            pdf.cell(200, 10, f"{key}: {value}", ln=True)
    else:
        print("Error: Unexpected data format from API.")
        return

    pdf.output(f"{name}_resume.pdf")
    print(f" Resume PDF generated: {name}_resume.pdf")

def get_args():
    parser = argparse.ArgumentParser(description="Generate a customizable resume PDF.")
    parser.add_argument("--name", type=str, required=True, help="Your name for the resume API")
    parser.add_argument("--font-size", type=int, default=12, help="Font size for resume text")
    parser.add_argument("--font-color", type=str, default="#000000", help="Font color (hex code)")
    parser.add_argument("--background-color", type=str, default="#FFFFFF", help="Background color (hex code)")
    
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    resume_data = fetch_resume(args.name)
    if resume_data:
        create_pdf(resume_data, args.font_size, args.font_color, args.background_color, args.name)
