class KayoProfile():
    def __init__(self,profile_object):
        self.id: str = profile_object.get("id",None)
        self.root_flag: bool = profile_object.get("root_flag",None)
        self.name: str =  profile_object.get("name", None)
        self.first_name: str = profile_object.get("first_name",None)
        self.last_name: str = profile_object.get("last_name",None)
        self.avatar_id: int = profile_object.get("avatar_id",None)
        self.onboarding_status: str = profile_object.get("onboarding_status",None)
        self.phone_number: str = profile_object.get("phone_number",None)
        self.email: str = profile_object.get("email",None)
