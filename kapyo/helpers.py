def validate_auth_session(auth_session):
    #Check if logged in
    if auth_session.token is not None:
        #Check if the tokens has expired
        if auth_session.is_token_expired():
            print('Token expired... Resetting')
            if auth_session.reset_token():
                print('Token Reset')
            else:
                return False
    else:
        print('No Token. Logging in...')
        if auth_session.login():
            print('Logged In')
        else:
            return False

    return True

