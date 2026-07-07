from fastapi import APIRouter, Depends

from app.api.schemas.reports import ReportCreate, ReportResponse
from app.api.services.report_service import ReportService


router = APIRouter(prefix="/reports", tags=["reports"])


def get_report_service():
    return ReportService()


@router.post("", response_model=ReportResponse, status_code=201)
def create_report(
    report: ReportCreate,
    service: ReportService = Depends(get_report_service),
):
    return service.create_report(report)
