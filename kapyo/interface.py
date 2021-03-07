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
    
    @property
    def profile(self):
        #Immutable Object
        return {
            'id':self.id,
            'root_flag':self.root_flag,
            'name':self.name,
            'first_name':self.first_name,
            'last_name':self.last_name,
            'avatar_id':self.avatar_id,
            'onboarding_status':self.onboarding_status,
            'phone_number':self.phone_number,
            'email': self.email
        }
    
    @profile.setter
    def profile(self, profile_object):
        self.__init__(profile_object)

    def __repr__(self):
        return str(self.profile)

    def __getitem__(self, key):
        return self.__getattribute__(key)

    def __setitem__(self, key, val):
        try:
            self.__setattr__(key, val)
        except AttributeError as ex:
            self.key = val

