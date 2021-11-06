import datetime
import pytest

class TestKayoAuthToken:
    @pytest.mark.freeze_time("2021-03-11 00:00")
    def test_token_expires_at(self,kayo_auth_token,constants):
        token_expires_in = constants["TOKEN_EXPIRES_IN"]
        assert kayo_auth_token.token_expires_at == datetime.datetime(2021, 3, 11,
                                                                     # HH:MM:SS calculation
                                                                     token_expires_in // 3600,
                                                                     token_expires_in % 3600 // 60,
                                                                     token_expires_in % 3600 % 60
                                                                     )

    @pytest.mark.freeze_time("2021-03-11 00:00")
    def test_is_token_expired(self,kayo_auth_token,freezer):
        freezer.move_to("2021-03-11 00:00")
        assert kayo_auth_token.is_token_expired == False
        freezer.move_to("2021-03-11 04:31")
        assert kayo_auth_token.is_token_expired == True
        freezer.move_to("2021-03-11 05:00")
        assert kayo_auth_token.is_token_expired == True
        freezer.move_to("3000-12-30 00:00")
        assert kayo_auth_token.is_token_expired == True


