from fastapi import APIRouter, Depends, HTTPException
from schema.openai.embeddings_models import EmbeddingsRequest, EmbeddingsResponse
from services.opeai_service import OpenAIService

router = APIRouter(
    prefix="/api/v1/openai",
    tags=["OpenAI"]
)


@router.post("/embeddings", response_model=EmbeddingsResponse)
async def create_embeddings(request: EmbeddingsRequest, openai_service: OpenAIService = Depends(OpenAIService)):
    """
    สร้าง embeddings จากข้อความที่ได้รับ
    
    Args:
        request: ข้อมูลคำขอ embeddings
        openai_service: บริการ OpenAI ที่ใช้เรียก API
        
    Returns:
        EmbeddingsResponse: ข้อมูลตอบกลับที่มี embeddings
    """
    try:
        return await openai_service.create_embeddings(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))