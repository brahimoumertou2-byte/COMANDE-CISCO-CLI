from fastapi import APIRouter, HTTPException

from ..schemas import GeneratorRequest, GeneratorResponse
from ..services.generator_service import GeneratorError, generate

router = APIRouter(prefix="/api/generator", tags=["generator"])


@router.post("", response_model=GeneratorResponse)
def generate_commands(payload: GeneratorRequest):
    try:
        commands, notes = generate(payload)
    except GeneratorError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return GeneratorResponse(technology=payload.technology, commands=commands, notes=notes)
