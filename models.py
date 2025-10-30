from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from enum import Enum

class PieceType(str, Enum):
    COAT = "colete"
    SWEATER = "blusa"
    HAT = "chapeu"
    SCARF = "cachecol"
    GLOVES = "luvas"
    SOCKS = "meias"
    BLANKET = "cobertor"
    BAG = "bolsa"

class Size(str, Enum):
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    XXL = "XXL"
    CUSTOM = "personalizado"

class ConversationState(BaseModel):
    current_step: str = "greeting"
    collected_data: Dict[str, Any] = {}
    missing_information: List[str] = []
    conversation_history: List[Dict[str, str]] = []

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[str] = None

class CrochetPattern(BaseModel):
    piece_type: str
    size: str
    color: str
    yarn_weight: str
    hook_size: str
    gauge: str
    materials: List[str]
    instructions: List[str]
    special_notes: List[str]
    difficulty_level: str
    estimated_time: str

class PatternRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
