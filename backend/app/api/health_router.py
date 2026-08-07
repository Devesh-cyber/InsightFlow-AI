from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("/")
def health():
    return {
        "status": "healthy",
        "message": "InsightFlow AI Backend Running"
    }