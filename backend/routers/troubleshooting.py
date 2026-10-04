from fastapi import APIRouter

from ..schemas import TroubleshootingRequest, TroubleshootingResponse, TroubleshootingFinding
from ..services.troubleshooting_service import analyze

router = APIRouter(prefix="/api/troubleshooting", tags=["troubleshooting"])


@router.post("", response_model=TroubleshootingResponse)
def troubleshoot(payload: TroubleshootingRequest):
    summary, raw_findings = analyze(payload.output, payload.context)
    findings = [
        TroubleshootingFinding(level=level, title=title, detail=detail)
        for level, title, detail in raw_findings
    ]
    return TroubleshootingResponse(summary=summary, findings=findings)
