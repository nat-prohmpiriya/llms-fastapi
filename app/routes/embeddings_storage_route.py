from fastapi import APIRouter, Depends, HTTPException
from schema.embeddings_storage_models import DocumentRequest, DocumentResponse, SearchRequest, SearchResponse, SearchResult
from schema.openai.embeddings_models import EmbeddingsRequest
from services.sqlite_service import SQLiteService
from services.opeai_service import OpenAIService
from typing import List

router = APIRouter(
    prefix="/api/v1/embeddings-storage",
    tags=["Embeddings Storage"]
)

# สร้างอินสแตนซ์ของ SQLiteService
sqlite_service = SQLiteService()

@router.post("/documents", response_model=DocumentResponse)
async def add_document(request: DocumentRequest, openai_service: OpenAIService = Depends(OpenAIService)):
    """
    เพิ่มเอกสารและสร้าง embedding ลงในฐานข้อมูล
    
    Args:
        request: ข้อมูลเอกสารที่ต้องการเพิ่ม
        openai_service: บริการ OpenAI
        
    Returns:
        DocumentResponse: ข้อมูลเอกสารที่เพิ่มแล้ว
    """
    try:
        # สร้าง embedding จากเนื้อหาเอกสาร
        embeddings_request = EmbeddingsRequest(
            input=request.content,
            model=request.model
        )
        
        embeddings_response = await openai_service.create_embeddings(embeddings_request)
        
        # เพิ่มเอกสารและ embedding ลงในฐานข้อมูล
        document_id = sqlite_service.add_document(
            content=request.content,
            embedding=embeddings_response.data[0].embedding,
            model=request.model,
            metadata=request.metadata
        )
        
        return DocumentResponse(
            document_id=document_id,
            content=request.content,
            metadata=request.metadata,
            model=request.model
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search", response_model=SearchResponse)
async def search_documents(request: SearchRequest, openai_service: OpenAIService = Depends(OpenAIService)):
    """
    ค้นหาเอกสารที่มีเนื้อหาคล้ายกับคำค้นหา
    
    Args:
        request: ข้อมูลคำค้นหา
        openai_service: บริการ OpenAI
        
    Returns:
        SearchResponse: ผลลัพธ์การค้นหา
    """
    try:
        # สร้าง embedding จากคำค้นหา
        embeddings_request = EmbeddingsRequest(
            input=request.query,
            model=request.model
        )
        
        embeddings_response = await openai_service.create_embeddings(embeddings_request)
        
        # ค้นหาเอกสารที่มี embedding ใกล้เคียง
        search_results = sqlite_service.search_similar(
            query_embedding=embeddings_response.data[0].embedding,
            model=request.model,
            top_k=request.top_k
        )
        
        # แปลงผลลัพธ์เป็นรูปแบบที่ต้องการ
        results = [
            SearchResult(
                document_id=result["document_id"],
                content=result["content"],
                metadata=result["metadata"],
                similarity=result["similarity"]
            )
            for result in search_results
        ]
        
        return SearchResponse(
            results=results,
            query=request.query,
            model=request.model
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: int):
    """
    ดึงข้อมูลเอกสารตาม ID
    
    Args:
        document_id: ID ของเอกสาร
        
    Returns:
        DocumentResponse: ข้อมูลเอกสาร
    """
    document = sqlite_service.get_document(document_id)
    if not document:
        raise HTTPException(status_code=404, detail=f"Document with ID {document_id} not found")
    
    return DocumentResponse(
        document_id=document["document_id"],
        content=document["content"],
        metadata=document["metadata"],
        model=document["model"]
    )

@router.delete("/documents/{document_id}")
async def delete_document(document_id: int):
    """
    ลบเอกสารตาม ID
    
    Args:
        document_id: ID ของเอกสาร
        
    Returns:
        dict: ข้อความยืนยันการลบ
    """
    success = sqlite_service.delete_document(document_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Document with ID {document_id} not found")
    
    return {"message": f"Document with ID {document_id} deleted successfully"}
