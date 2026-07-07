from fastapi import APIRouter, HTTPException, status

from app.api.models.supabase_report_model import SupabaseReportModel
from app.api.schemas.auth import LoginRequest, LoginResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):
    model = SupabaseReportModel()
    user = model.authenticate(request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas.",
        )
    return LoginResponse(user_id=str(user.get("id", "")), username=user.get("username", ""))
