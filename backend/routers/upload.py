"""
PDF Upload and Text Extraction Router.
"""

import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from models.schemas import DocumentInfo
from services.pdf_parser import extract_text_from_pdf, chunk_extracted_text

router = APIRouter()

@router.post("/upload", response_model=DocumentInfo)
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file, extract its text content, chunk it, and store it in memory.
    """
    # Import main store here to avoid circular imports
    from main import documents_store
    
    # 1. Validate file extension
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Only PDF files are supported."
        )
        
    # 2. Read file content
    try:
        contents = await file.read()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to read file: {str(e)}"
        )
        
    # 3. Parse PDF and extract text
    try:
        pages_content = extract_text_from_pdf(contents)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Failed to parse PDF document. It might be corrupted or malformed. Error: {str(e)}"
        )
        
    # Check if we got any pages
    if not pages_content:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="The uploaded PDF does not contain any readable pages."
        )
        
    # Check if there is actual text extracted (scanned vs text PDF check)
    total_chars = sum(len(page["text"]) for page in pages_content)
    if total_chars == 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No readable text found in PDF. Scanned/image-only PDFs are not supported."
        )
        
    # 4. Chunk text for LLM
    try:
        chunks = chunk_extracted_text(pages_content)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to chunk extracted text: {str(e)}"
        )
        
    # 5. Generate document ID and store chunks
    doc_id = str(uuid.uuid4())
    documents_store[doc_id] = {
        "filename": file.filename,
        "chunks": chunks,
        "page_count": len(pages_content),
        "total_characters": total_chars
    }
    
    return DocumentInfo(
        document_id=doc_id,
        filename=file.filename,
        page_count=len(pages_content),
        chunk_count=len(chunks),
        total_characters=total_chars
    )
