from pydantic import BaseModel, ConfigDict, Field


class CommandBase(BaseModel):
    command: str = Field(min_length=1)
    category: str
    device: str = "Router"
    mode: str = "Privileged EXEC"
    description: str
    syntax: str
    example: str
    platform: str = "Cisco IOS / IOS XE"


class CommandCreate(CommandBase):
    pass


class CommandRead(CommandBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class GeneratorRequest(BaseModel):
    technology: str
    router_id: str | None = None
    process_id: int | None = None
    network: str | None = None
    area: int | None = None
    destination: str | None = None
    mask: str | None = None
    next_hop: str | None = None
    interface: str | None = None


class GeneratorResponse(BaseModel):
    technology: str
    commands: list[str]
    notes: list[str] = []


class TroubleshootingRequest(BaseModel):
    output: str = Field(min_length=1)
    context: str | None = None


class TroubleshootingFinding(BaseModel):
    level: str
    title: str
    detail: str


class TroubleshootingResponse(BaseModel):
    summary: str
    findings: list[TroubleshootingFinding]
