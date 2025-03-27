from pydantic import BaseModel
from typing import List, Optional

class TTSRequest(BaseModel):
    text: str
    model: str = "mesolitica/VITS-osman"
    temperature: float = 0.6666
    length_ratio: float = 1.0

class TTSResponse(BaseModel):
    filename: str
    audio_url: str

class TTSBatchRequest(BaseModel):
    lines: List[str]
    model: str = "mesolitica/VITS-osman"
    temperature: float = 0.6666
    length_ratio: float = 1.0

class TTSBatchResponse(BaseModel):
    files: List[TTSResponse]

class VoiceModel(BaseModel):
    name: str
    display_name: str
    size_mb: int
    understands_punctuation: bool
    is_lowercase: bool