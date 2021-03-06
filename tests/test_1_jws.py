import json
from jwkest.jwk import SYM_key, RSA_key
from jwkest.jws import SIGNER_ALGS
from jwkest.jws import JWS

__author__ = 'rohe0002'

import jwkest
from jwkest import jws
from jwkest import b64e

KEY = "certs/server.key"


def rsa_load(filename):
    """Read a PEM-encoded RSA key pair from a file.
        - same code as :
            https://github.com/rohe/pyoidc/blob/master/src/oic/utils/keyio.py
    """
    import M2Crypto
    return M2Crypto.RSA.load_key(filename, M2Crypto.util.no_passphrase_callback)

JWK = {"keys": [{'alg': 'RSA',
                 'use': 'foo',
                 'e': 'AQAB',
                 'n': 'wf-wiusGhA-gleZYQAOPQlNUIucPiqXdPVyieDqQbXXOPBe3nuggtVzeq7pVFH1dZz4dY2Q2LA5DaegvP8kRvoSB_87ds3dy3Rfym_GUSc5B0l1TgEobcyaep8jguRoHto6GWHfCfKqoUYZq4N8vh4LLMQwLR6zi6Jtu82nB5k8'}]}

HMAC_KEY = [3, 35, 53, 75, 43, 15, 165, 188, 131, 126, 6, 101, 119, 123, 166,
            143, 90, 179, 40, 230, 240, 84, 201, 40, 169, 15, 132, 178, 210, 80,
            46, 191, 211, 251, 90, 146, 210, 6, 71, 239, 150, 138, 180, 195,
            119, 98, 61, 34, 61, 46, 33, 114, 5, 46, 79, 8, 192, 205, 154, 245,
            103, 208, 128, 163]


def test_1():
    claimset = {"iss": "joe",
                "exp": 1300819380,
                "http://example.com/is_root": True}

    _jws = JWS(claimset, cty="JWT")
    _jwt = _jws.sign_compact()

    _jr = JWS()
    _jr.verify_compact(_jwt)
    print _jr
    assert _jr.alg == u'none'
    assert _jr.msg == {"iss": "joe",
                       "exp": 1300819380,
                       "http://example.com/is_root": True}


def test_hmac_256():
    payload = "Please take a moment to register today"
    keys = [SYM_key(key=jwkest.intarr2bin(HMAC_KEY))]
    _jws = JWS(payload, alg="HS256")
    _jwt = _jws.sign_compact(keys)

    info = JWS().verify_compact(_jwt, keys)

    assert info == payload


def test_hmac_384():
    payload = "Please take a moment to register today"
    keys = [SYM_key(key="My hollow echo")]
    _jws = JWS(payload, alg="HS256")
    _jwt = _jws.sign_compact(keys)

    _rj = JWS()
    info = _rj.verify_compact(_jwt, keys)

    assert info == payload


def test_hmac_512():
    payload = "Please take a moment to register today"
    keys = [SYM_key(key="My hollow echo")]
    _jws = JWS(payload, alg="HS256")
    _jwt = _jws.sign_compact(keys)

    _rj = JWS()
    info = _rj.verify_compact(_jwt, keys)
    assert info == payload


def test_left_hash_hs256():
    hsh = jws.left_hash("Please take a moment to register today")
    assert hsh == "rCFHVJuxTqRxOsn2IUzgvA"


def test_left_hash_hs512():
    hsh = jws.left_hash("Please take a moment to register today", "HS512")
    assert hsh == "_h6feWLt8zbYcOFnaBmekTzMJYEHdVTaXlDgJSWsEeY"


def test_rs256():
    payload = "Please take a moment to register today"
    keys = [RSA_key(key=rsa_load(KEY))]
    keys[0]._keytype = "private"
    _jws = JWS(payload, alg="RS256")
    _jwt = _jws.sign_compact(keys)

    _rj = JWS()
    info = _rj.verify_compact(_jwt, keys)

    assert info == payload


def test_rs384():
    payload = "Please take a moment to register today"
    keys = [RSA_key(key=rsa_load(KEY))]
    keys[0]._keytype = "private"
    _jws = JWS(payload, alg="RS384")
    _jwt = _jws.sign_compact(keys)

    _rj = JWS()
    info = _rj.verify_compact(_jwt, keys)
    assert info == payload


def test_rs512():
    payload = "Please take a moment to register today"
    keys = [RSA_key(key=rsa_load(KEY))]
    keys[0]._keytype = "private"
    _jws = JWS(payload, alg="RS512")
    _jwt = _jws.sign_compact(keys)

    _rj = JWS()
    info = _rj.verify_compact(_jwt, keys)
    assert info == payload


def test_a_1_1a():
    header = '{"typ":"JWT",\r\n "alg":"HS256"}'
    val = b64e(header)
    assert val == "eyJ0eXAiOiJKV1QiLA0KICJhbGciOiJIUzI1NiJ9"


def test_a_1_1b():
    payload = '{"iss":"joe",\r\n "exp":1300819380,\r\n "http://example.com/is_root":true}'
    val = b64e(payload)
    assert val == "eyJpc3MiOiJqb2UiLA0KICJleHAiOjEzMDA4MTkzODAsDQogImh0dHA6Ly9leGFtcGxlLmNvbS9pc19yb290Ijp0cnVlfQ"


def test_a_1_1c():
    hmac = jwkest.intarr2bin(HMAC_KEY)
    signer = SIGNER_ALGS["HS256"]
    header = '{"typ":"JWT",\r\n "alg":"HS256"}'
    payload = '{"iss":"joe",\r\n "exp":1300819380,\r\n "http://example.com/is_root":true}'
    sign_input = b64e(header) + '.' + b64e(payload)
    sig = signer.sign(sign_input, hmac)
    assert b64e(sig) == "dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"


def test_a_1_3a():
    _jwt = "eyJ0eXAiOiJKV1QiLA0KICJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJqb2UiLA0KICJleHAiOjEzMDA4MTkzODAsDQogImh0dHA6Ly9leGFtcGxlLmNvbS9pc19yb290Ijp0cnVlfQ.dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"

    #keycol = {"hmac": jwkest.intarr2bin(HMAC_KEY)}
    header, claim, crypto, header_b64, claim_b64 = jwkest.unpack(_jwt)

    hmac = jwkest.intarr2bin(HMAC_KEY)
    signer = SIGNER_ALGS["HS256"]
    info = signer.verify(header_b64 + '.' + claim_b64, crypto, hmac)


def test_a_1_3b():
    _jwt = "eyJ0eXAiOiJKV1QiLA0KICJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJqb2UiLA0KICJleHAiOjEzMDA4MTkzODAsDQogImh0dHA6Ly9leGFtcGxlLmNvbS9pc19yb290Ijp0cnVlfQ.dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"
    keys = [SYM_key(key=jwkest.intarr2bin(HMAC_KEY))]
    _jws2 = JWS()
    _jws2.verify_compact(_jwt, keys)


def test_jws_1():
    msg = {"iss": "joe", "exp": 1300819380, "http://example.com/is_root": True}
    jwk = SYM_key(key=jwkest.intarr2bin(HMAC_KEY))
    jwk.decomp()
    _jws = JWS(msg, cty="JWT", alg="HS256", jwk=json.dumps(jwk.to_dict()))
    res = _jws.sign_compact()

    _jws2 = JWS()
    _jws2.verify_compact(res)
    assert _jws2.msg == msg

if __name__ == "__main__":
    test_jws_1()