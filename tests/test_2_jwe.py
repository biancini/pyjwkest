import hashlib
import M2Crypto
from jwkest.jwk import RSA_key
from aes_key_wrap_crypto import aes_wrap_key

__author__ = 'rohe0002'

from M2Crypto import RSA

from jwkest import b64e
from jwkest.jwe import JWE_RSA
from jwkest.jwe import JWE
from jwkest.jwe import ENC2ALG
from jwkest.jwe import aes_enc
from jwkest.jwe import int2bigendian
from jwkest.jwe import ciphertext_and_authentication_tag
from jwkest.jws import SIGNER_ALGS
from jwkest.gcm import gcm_encrypt


def intarr2str(arr):
    return "".join([chr(c) for c in arr])


def str2intarr(txt):
    return [ord(c) for c in txt]


def test_jwe_09_a1():
    # RSAES OAEP and AES GCM
    msg = "The true sign of intelligence is not knowledge but imagination."

    # A.1.1
    header = '{"alg":"RSA-OAEP","enc":"A256GCM"}'
    b64_header = b64e(header)

    # A.1.2
    assert b64_header == "eyJhbGciOiJSU0EtT0FFUCIsImVuYyI6IkEyNTZHQ00ifQ"

    # A.1.3
    cek = intarr2str([177, 161, 244, 128, 84, 143, 225, 115, 63, 180, 3, 255,
                      107, 154, 212, 246, 138, 7, 110, 91, 112, 46, 34, 105, 47,
                      130, 203, 46, 122, 234, 64, 252])

    # A.1.4 Key Encryption
    enc_key = [
        56, 163, 154, 192, 58, 53, 222, 4, 105, 218, 136, 218, 29, 94, 203,
        22, 150, 92, 129, 94, 211, 232, 53, 89, 41, 60, 138, 56, 196, 216,
        82, 98, 168, 76, 37, 73, 70, 7, 36, 8, 191, 100, 136, 196, 244, 220,
        145, 158, 138, 155, 4, 117, 141, 230, 199, 247, 173, 45, 182, 214,
        74, 177, 107, 211, 153, 11, 205, 196, 171, 226, 162, 128, 171, 182,
        13, 237, 239, 99, 193, 4, 91, 219, 121, 223, 107, 167, 61, 119, 228,
        173, 156, 137, 134, 200, 80, 219, 74, 253, 56, 185, 91, 177, 34, 158,
        89, 154, 205, 96, 55, 18, 138, 43, 96, 218, 215, 128, 124, 75, 138,
        243, 85, 25, 109, 117, 140, 26, 155, 249, 67, 167, 149, 231, 100, 6,
        41, 65, 214, 251, 232, 87, 72, 40, 182, 149, 154, 168, 31, 193, 126,
        215, 89, 28, 111, 219, 125, 182, 139, 235, 195, 197, 23, 234, 55, 58,
        63, 180, 68, 202, 206, 149, 75, 205, 248, 176, 67, 39, 178, 60, 98,
        193, 32, 238, 122, 96, 158, 222, 57, 183, 111, 210, 55, 188, 215,
        206, 180, 166, 150, 166, 106, 250, 55, 229, 72, 40, 69, 214, 216,
        104, 23, 40, 135, 212, 28, 127, 41, 80, 175, 174, 168, 115, 171, 197,
        89, 116, 92, 103, 246, 83, 216, 182, 176, 84, 37, 147, 35, 45, 219,
        172, 99, 226, 233, 73, 37, 124, 42, 72, 49, 242, 35, 127, 184, 134,
        117, 114, 135, 206]

    b64_ejek = "ApfOLCaDbqs_JXPYy2I937v_xmrzj-Iss1mG6NAHmeJViM6j2l0MHvfseIdHVyU2BIoGVu9ohvkkWiRq5DL2jYZTPA9TAdwq3FUIVyoH-Pedf6elHIVFi2KGDEspYMtQARMMSBcS7pslx6flh1Cfh3GBKysztVMEhZ_maFkm4PYVCsJsvq6Ct3fg2CJPOs0X1DHuxZKoIGIqcbeK4XEO5a0h5TAuJObKdfO0dKwfNSSbpu5sFrpRFwV2FTTYoqF4zI46N9-_hMIznlEpftRXhScEJuZ9HG8C8CHB1WRZ_J48PleqdhF4o7fB5J1wFqUXBtbtuGJ_A2Xe6AEhrlzCOw"

    iv = intarr2str([227, 197, 117, 252, 2, 219, 233, 68, 180, 225, 77, 219])

    aadp = b64_header + b'.' + b64_ejek
    
    ctxt, tag = gcm_encrypt(cek, iv, msg, aadp)

    _va = [ord(c) for c in ctxt]
    assert _va == [229, 236, 166, 241, 53, 191, 115, 196, 174, 43, 73, 109, 39,
                   122, 233, 96, 140, 206, 120, 52, 51, 237, 48, 11, 190, 219,
                   186, 80, 111, 104, 50, 142, 47, 167, 59, 61, 181, 127, 196,
                   21, 40, 82, 242, 32, 123, 143, 168, 226, 73, 216, 176, 144,
                   138, 247, 106, 60, 16, 205, 160, 109, 64, 63, 192]
    assert [ord(c) for c in tag] == [130, 17, 32, 198, 120, 167, 144, 113, 0,
                                     50, 158, 49, 102, 208, 118, 152]

    res = b".".join([b64_header, b64_ejek, b64e(iv), b64e(ctxt), b64e(tag)])

    assert res == "".join([
        "eyJhbGciOiJSU0EtT0FFUCIsImVuYyI6IkEyNTZHQ00ifQ.",
        "ApfOLCaDbqs_JXPYy2I937v_xmrzj-Iss1mG6NAHmeJViM6j2l0MHvfseIdHVyU2",
        "BIoGVu9ohvkkWiRq5DL2jYZTPA9TAdwq3FUIVyoH-Pedf6elHIVFi2KGDEspYMtQ",
        "ARMMSBcS7pslx6flh1Cfh3GBKysztVMEhZ_maFkm4PYVCsJsvq6Ct3fg2CJPOs0X",
        "1DHuxZKoIGIqcbeK4XEO5a0h5TAuJObKdfO0dKwfNSSbpu5sFrpRFwV2FTTYoqF4",
        "zI46N9-_hMIznlEpftRXhScEJuZ9HG8C8CHB1WRZ_J48PleqdhF4o7fB5J1wFqUX",
        "BtbtuGJ_A2Xe6AEhrlzCOw.",
        "48V1_ALb6US04U3b.",
        "5eym8TW_c8SuK0ltJ3rpYIzOeDQz7TALvtu6UG9oMo4vpzs9tX_EFShS8iB7j6ji",
        "SdiwkIr3ajwQzaBtQD_A.",
        "ghEgxninkHEAMp4xZtB2mA"])


def sha256_digest(msg):
    return hashlib.sha256(msg).digest()


def test_jwe_09_a3():
    #Example JWE using AES Key Wrap and AES GCM

    msg = "Live long and prosper."

    header = '{"alg":"A128KW","enc":"A128CBC-HS256"}'
    b64_header = b64e(header)

    assert b64_header == "eyJhbGciOiJBMTI4S1ciLCJlbmMiOiJBMTI4Q0JDLUhTMjU2In0"

    cek = intarr2str([4, 211, 31, 197, 84, 157, 252, 254, 11, 100, 157, 250,
                      63, 170, 106, 206, 107, 124, 212, 45, 111, 107, 9, 219,
                      200, 177, 0, 240, 143, 156, 44, 207])

    shared_key = [25, 172, 32, 130, 225, 114, 26, 181, 138, 106, 254, 192, 95,
                  133, 74, 82]


    jek = aes_wrap_key(intarr2str(shared_key), cek)

    assert str2intarr(jek) == [
        232, 160, 123, 211, 183, 76, 245, 132, 200, 128, 123, 75, 190, 216,
        22, 67, 201, 138, 193, 186, 9, 91, 122, 31, 246, 90, 28, 139, 57, 3,
        76, 124, 193, 11, 98, 37, 173, 61, 104, 57]

    b64_jek = b64e(jek)
    assert b64_jek == "6KB707dM9YTIgHtLvtgWQ8mKwboJW3of9locizkDTHzBC2IlrT1oOQ"

    iv = intarr2str([3, 22, 60, 12, 43, 67, 104, 105, 108, 108, 105, 99, 111,
                     116, 104, 101])

    b64_iv = b64e(iv)
    assert b64_iv == "AxY8DCtDaGlsbGljb3RoZQ"

    aadp = b64_header

    assert str2intarr(aadp) == [101, 121, 74, 104, 98, 71, 99, 105, 79, 105,
                                74, 66, 77, 84, 73, 52, 83, 49, 99, 105, 76,
                                67, 74, 108, 98, 109, 77, 105, 79, 105, 74, 66,
                                77, 84, 73, 52, 81, 48, 74, 68, 76, 85, 104, 84,
                                77, 106, 85, 50, 73, 110, 48]

    ctxt, tag = ciphertext_and_authentication_tag(msg, cek, aadp, iv,
                                                  algo="A128CBC-HS256")

    assert str2intarr(ctxt) == [
        40, 57, 83, 181, 119, 33, 133, 148, 198, 185, 243, 24, 152, 230, 6,
        75, 129, 223, 127, 19, 210, 82, 183, 230, 168, 33, 215, 104, 143,
        112, 56, 102]

    assert str2intarr(tag) == [83, 73, 191, 98, 104, 205, 211, 128, 201, 189,
                               199, 133, 32, 38, 194, 85]

    enc_cipher_text = b64e(ctxt)
    assert enc_cipher_text == "KDlTtXchhZTGufMYmOYGS4HffxPSUrfmqCHXaI9wOGY"

    enc_authn_tag = b64e(tag)
    assert enc_authn_tag == "U0m_YmjN04DJvceFICbCVQ"


def test_jwe_09_b():
    #AES_128_CBC_HMAC_SHA_256 computation

    key = intarr2str([4, 211, 31, 197, 84, 157, 252, 254, 11, 100, 157, 250, 63,
                      170, 106, 206, 107, 124, 212, 45, 111, 107, 9, 219, 200,
                      177, 0, 240, 143, 156, 44, 207])

    mac_key = key[:16]
    enc_key = key[16:]

    msg = intarr2str([76, 105, 118, 101, 32, 108, 111, 110, 103, 32, 97, 110,
                      100, 32, 112, 114, 111, 115, 112, 101, 114, 46])

    ivv = [3, 22, 60, 12, 43, 67, 104, 105, 108, 108, 105, 99, 111, 116, 104,
           101]

    ivv_str = intarr2str(ivv)

    # Encrypt the Plaintext with AES in Cipher Block Chaining (CBC) mode
    # using PKCS #5 padding using the enc_key above.

    c = M2Crypto.EVP.Cipher(alg=ENC2ALG["A128CBC"], key=enc_key,
                            iv=ivv_str, op=1)

    ctxt = aes_enc(c, msg)

    assert str2intarr(ctxt) == [40, 57, 83, 181, 119, 33, 133, 148, 198, 185,
                                243, 24, 152, 230, 6, 75, 129, 223, 127, 19,
                                210, 82, 183, 230, 168, 33, 215, 104, 143,
                                112, 56, 102]

    aad = [101, 121, 74, 104, 98, 71, 99, 105, 79, 105, 74, 66, 77,
           84, 73, 52, 83, 49, 99, 105, 76, 67, 74, 108, 98, 109, 77,
           105, 79, 105, 74, 66, 77, 84, 73, 52, 81, 48, 74, 68, 76,
           85, 104, 84, 77, 106, 85, 50, 73, 110, 48, 46, 54, 75, 66,
           55, 48, 55, 100, 77, 57, 89, 84, 73, 103, 72, 116, 76,
           118, 116, 103, 87, 81, 56, 109, 75, 119, 98, 111, 74, 87,
           51, 111, 102, 57, 108, 111, 99, 105, 122, 107, 68, 84, 72,
           122, 66, 67, 50, 73, 108, 114, 84, 49, 111, 79, 81]

    al = int2bigendian(len(aad) * 8)
    while len(al) < 8:
        al.insert(0, 0)

    _inp = aad + ivv + str2intarr(ctxt) + al

    assert _inp == [101, 121, 74, 104, 98, 71, 99, 105, 79, 105, 74, 66, 77, 84,
                    73, 52, 83, 49, 99, 105, 76, 67, 74, 108, 98, 109, 77, 105,
                    79, 105, 74, 66, 77, 84, 73, 52, 81, 48, 74, 68, 76, 85,
                    104, 84, 77, 106, 85, 50, 73, 110, 48, 46, 54, 75, 66, 55,
                    48, 55, 100, 77, 57, 89, 84, 73, 103, 72, 116, 76, 118, 116,
                    103, 87, 81, 56, 109, 75, 119, 98, 111, 74, 87, 51, 111,
                    102, 57, 108, 111, 99, 105, 122, 107, 68, 84, 72, 122, 66,
                    67, 50, 73, 108, 114, 84, 49, 111, 79, 81, 3, 22, 60, 12,
                    43, 67, 104, 105, 108, 108, 105, 99, 111, 116, 104, 101, 40,
                    57, 83, 181, 119, 33, 133, 148, 198, 185, 243, 24, 152, 230,
                    6, 75, 129, 223, 127, 19, 210, 82, 183, 230, 168, 33, 215,
                    104, 143, 112, 56, 102, 0, 0, 0, 0, 0, 0, 3, 80]

    func = SIGNER_ALGS["HS256"]
    m = func.sign(intarr2str(_inp), mac_key)
    mi = str2intarr(m)
    assert mi == [8, 65, 248, 101, 45, 185, 28, 218, 232, 112, 83, 79, 84, 221,
                  18, 172, 50, 145, 207, 8, 14, 74, 44, 220, 100, 117, 32, 57,
                  239, 149, 173, 226]


def gen_callback(*args):
    pass


rsa = RSA.gen_key(2048, 65537, gen_callback)
plain = "Now is the time for all good men to come to the aid of their country."


def test_rsa_encrypt_decrypt_rsa_cbc():
    _rsa = JWE_RSA(plain, alg="RSA1_5", enc="A128CBC-HS256")
    jwt = _rsa.encrypt(rsa)
    dec = JWE_RSA()
    msg = dec.decrypt(jwt, rsa, "private")

    assert msg == plain


def test_rsa_encrypt_decrypt_rsa_oaep_gcm():
    jwt = JWE_RSA(plain, alg="RSA-OAEP", enc="A256GCM").encrypt(rsa)
    msg = JWE_RSA().decrypt(jwt, rsa, "private")

    assert msg == plain


def test_encrypt_decrypt_rsa_cbc():
    _key = RSA_key(key=rsa)
    _key._keytype = "private"
    _jwe0 = JWE(plain, alg="RSA1_5", enc="A128CBC-HS256")

    jwt = _jwe0.encrypt([_key], "public")

    _jwe1 = JWE()
    msg = _jwe1.decrypt(jwt, [_key], "private")

    assert msg == plain


if __name__ == "__main__":
    test_encrypt_decrypt_rsa_cbc()
