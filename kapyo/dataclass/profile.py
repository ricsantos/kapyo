from dataclasses import dataclass

@dataclass
class KayoProfile:
    id: str
    root_flag: bool
    name: str
    first_name: str
    last_name: str
    avatar_id: int
    onboarding_status: str
    phone_number: str
    email: str