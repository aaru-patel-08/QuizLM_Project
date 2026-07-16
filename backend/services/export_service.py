"""
Quiz Export Service.
Generates JSON, Markdown, and styled PDF files from Quiz structures.
"""

import json
from fpdf import FPDF
from models.schemas import Quiz, Question

def export_json(quiz: Quiz) -> str:
    """Serializes the quiz to a formatted JSON string."""
    # Use standard dict export from pydantic
    return quiz.model_dump_json(indent=2)

def export_markdown(quiz: Quiz) -> str:
    """Renders the quiz as a clean, readable Markdown document."""
    md = []
    md.append(f"# {quiz.title}")
    md.append(f"**Source Document:** {quiz.source_filename}")
    md.append(f"**Difficulty:** {quiz.difficulty.capitalize()}")
    md.append(f"**Questions:** {len(quiz.questions)}")
    md.append("")
    md.append("---")
    md.append("")
    
    # Render Questions
    for idx, q in enumerate(quiz.questions):
        md.append(f"### Q{idx + 1}. {q.question}")
        md.append(f"*Type: {q.type.replace('_', ' ').capitalize()}* | *Source: {q.source_reference}*")
        md.append("")
        
        if q.type in ["multiple_choice", "true_false"] and q.options:
            for opt_idx, opt in enumerate(q.options):
                # Letter options (A, B, C, D)
                letter = chr(65 + opt_idx) # 65 is 'A'
                md.append(f"- **{letter})** {opt}")
            md.append("")
            
        elif q.type == "short_answer":
            md.append("*Write your answer below:*")
            md.append("\n\n\n") # Leave space for writing
            md.append("")
            
    md.append("---")
    md.append("")
    md.append("## Answer Key & Explanations")
    md.append("")
    
    for idx, q in enumerate(quiz.questions):
        md.append(f"### Q{idx + 1}")
        md.append(f"**Correct Answer:** {q.correct_answer}")
        md.append(f"**Explanation:** {q.explanation}")
        md.append("")
        
    return "\n".join(md)

class StyledQuizPDF(FPDF):
    """Custom FPDF class for styled Quiz PDFs."""
    def header(self):
        # Top margin spacing
        self.set_font('Helvetica', 'B', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, 'AI QUIZ GENERATOR', 0, 0, 'R')
        self.ln(10)
        
    def footer(self):
        # Page numbers
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def export_pdf(quiz: Quiz) -> bytes:
    """Renders the quiz as a beautiful styled PDF."""
    pdf = StyledQuizPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # 1. Title Block
    pdf.set_font('Helvetica', 'B', 20)
    pdf.set_text_color(40, 44, 52) # Dark grey/blue
    pdf.multi_cell(0, 10, quiz.title)
    pdf.ln(5)
    
    # 2. Metadata Info
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, f"Source File: {quiz.source_filename}", ln=True)
    pdf.cell(0, 5, f"Difficulty: {quiz.difficulty.capitalize()}", ln=True)
    pdf.cell(0, 5, f"Number of Questions: {len(quiz.questions)}", ln=True)
    pdf.ln(10)
    
    # Draw horizontal divider
    pdf.set_draw_color(220, 224, 230)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(8)
    
    # 3. Render Questions
    pdf.set_text_color(40, 44, 52)
    for idx, q in enumerate(quiz.questions):
        # Question Title
        pdf.set_font('Helvetica', 'B', 12)
        # Using multi_cell to handle wrapping
        pdf.multi_cell(0, 6, f"Q{idx + 1}. {q.question}")
        
        # Metadata / Reference info
        pdf.set_font('Helvetica', 'I', 9)
        pdf.set_text_color(120, 120, 120)
        q_type_str = q.type.replace('_', ' ').capitalize()
        pdf.cell(0, 5, f"Type: {q_type_str}  |  Source: {q.source_reference}", ln=True)
        pdf.ln(2)
        
        pdf.set_text_color(40, 44, 52)
        pdf.set_font('Helvetica', '', 11)
        # Render Options
        if q.type in ["multiple_choice", "true_false"] and q.options:
            for opt_idx, opt in enumerate(q.options):
                letter = chr(65 + opt_idx)
                # Option text
                pdf.multi_cell(0, 6, f"  [{letter}]  {opt}")
            pdf.ln(6)
        elif q.type == "short_answer":
            # Draw a dotted or blank area for writing
            pdf.ln(2)
            pdf.set_draw_color(200, 200, 200)
            # Add lines for student answer
            for _ in range(3):
                current_y = pdf.get_y()
                pdf.line(15, current_y + 5, 195, current_y + 5)
                pdf.ln(8)
            pdf.ln(4)
            
    # Add page break for answer key
    pdf.add_page()
    
    # 4. Answer Key
    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_text_color(40, 44, 52)
    pdf.cell(0, 10, "Answer Key & Explanations", ln=True)
    pdf.ln(5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(8)
    
    for idx, q in enumerate(quiz.questions):
        pdf.set_font('Helvetica', 'B', 11)
        pdf.multi_cell(0, 5, f"Q{idx + 1} Correct Answer: {q.correct_answer}")
        
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(80, 80, 80)
        pdf.multi_cell(0, 5, f"Explanation: {q.explanation}")
        pdf.ln(4)
        pdf.set_text_color(40, 44, 52)
        
    return bytes(pdf.output())
