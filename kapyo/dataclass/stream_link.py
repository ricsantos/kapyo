from dataclasses import dataclass

@dataclass
class KayoStreamLink():
    id: str
    bitrate: str
    media_format: str
    mime_type: str
    headers: str
    uri: str

