"""
PDF text extraction and chunking service.
Uses PyMuPDF (fitz) to extract text and chunks pages for LLM context compatibility.
"""

import io
import fitz  # PyMuPDF
from typing import List
from models.schemas import PageChunk

def extract_text_from_pdf(pdf_bytes: bytes) -> List[dict]:
    """
    Extracts text page by page from PDF bytes.
    Returns a list of dicts with 'page_number' and 'text'.
    """
    pages_content = []
    
    # Load PDF using PyMuPDF from bytes
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    
    for page_idx in range(len(doc)):
        page = doc.load_page(page_idx)
        text = page.get_text("text")  # "text" layout preserves general order well
        
        pages_content.append({
            "page_number": page_idx + 1,
            "text": text.strip()
        })
        
    return pages_content

def chunk_extracted_text(pages_content: List[dict], max_chars: int = 6000, overlap_chars: int = 500) -> List[PageChunk]:
    """
    Chunks extracted pages into reasonable text sizes, preserving page markers.
    """
    chunks = []
    chunk_index = 0
    
    current_chunk_text = ""
    current_start_page = 0
    current_end_page = 0
    
    for page in pages_content:
        page_num = page["page_number"]
        page_text = page["text"]
        
        # Skip empty pages
        if not page_text:
            continue
            
        page_marker = f"\n--- [Page {page_num}] ---\n"
        
        # If adding this page exceeds max_chars, save the current chunk first
        if current_chunk_text and len(current_chunk_text) + len(page_marker) + len(page_text) > max_chars:
            chunks.append(PageChunk(
                text=current_chunk_text.strip(),
                page_start=current_start_page,
                page_end=current_end_page,
                chunk_index=chunk_index
            ))
            chunk_index += 1
            
            # Keep overlap from previous chunk
            overlap_start = max(0, len(current_chunk_text) - overlap_chars)
            current_chunk_text = current_chunk_text[overlap_start:]
            # Keep start page as page_num or current_end_page
            current_start_page = current_end_page
            
        if not current_chunk_text or current_chunk_text.isspace():
            current_chunk_text = page_marker + page_text
            current_start_page = page_num
        else:
            current_chunk_text += page_marker + page_text
            
        current_end_page = page_num
        
    # Append the last chunk if it exists
    if current_chunk_text.strip():
        chunks.append(PageChunk(
            text=current_chunk_text.strip(),
            page_start=current_start_page,
            page_end=current_end_page,
            chunk_index=chunk_index
        ))
        
    return chunks
