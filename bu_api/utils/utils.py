from base64 import b64decode
from flask import request, make_response, jsonify
from flask_restx import reqparse, fields
from functools import wraps


def get_user_credentials(auth_header):
    if auth_header[0] != 'Basic':
        return auth_header[0].split(':')
    return b64decode(auth_header[1].encode()).decode().split(':')


def auth_required(funct):
    @wraps(funct)
    def decorated_function(*args, **kwargs):
        try:
            user, secret = get_user_credentials(request.headers['Authorization'].split())
            if user != 'testuser':
                raise Exception('Invalid username provided')
            if secret != 'T3st9paS$w0rd!':
                raise Exception('Invalid credentials provided')
        except Exception as err:
            return make_response(jsonify({'ERROR': str(err)}), 401)
        return funct(*args, **kwargs)
    return decorated_function()


def get_models_parsers(api):

    get_file_parser = reqparse.RequestParser()
    get_file_parser.add_argument(
        'FileName',
        type=str,
        location='headers',
        required=True
    )

    post_file_model = api.model(
        'admin_update_schema_fields', {
            'FileData': fields.Raw(required=True),
        }
    )

    return get_file_parser, post_file_model


def get_example_certs():

    cert_1 = """
MIIDYjCCAkoCCQD12xSERbXFIDANBgkqhkiG9w0BAQsFADBzMQswCQYDVQQGEwJV
UzELMAkGA1UECAwCTUExDzANBgNVBAcMBkJvc3RvbjEWMBQGA1UECgwNb3RoZXJ0
ZXN0LmNvbTEWMBQGA1UECwwNb3RoZXJ0ZXN0LmNvbTEWMBQGA1UEAwwNb3RoZXJ0
ZXN0LmNvbTAeFw0yMTA0MTgyMTE2MTFaFw0yMjA0MTgyMTE2MTFaMHMxCzAJBgNV
BAYTAlVTMQswCQYDVQQIDAJNQTEPMA0GA1UEBwwGQm9zdG9uMRYwFAYDVQQKDA1v
dGhlcnRlc3QuY29tMRYwFAYDVQQLDA1vdGhlcnRlc3QuY29tMRYwFAYDVQQDDA1v
dGhlcnRlc3QuY29tMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA8cHf
ZArgtNlhmnxZmzaUgk4Yiln01CKBIF/WroXjUub6c7jE0zmaAjFya46vtbMto9RT
qgDPl2iDALyqEfImZGb3H+/EhLM8h+qU8kjZNDCnH/JiOa4DFrtzqxw40exSuN/y
umcmDSGxLG0YjpbpFp+umkLv6GbX/OFXWvRcavNLrs1utcslv956aFLM7I4rv5jT
3mBvsWxDZ4Yj/PUIKbfQnEJ2P8NsFAq24NrOmaIgaBO5+/7PqpV5sjPAyV2S/fL/
pVrQZ0997l6GbP5taTucciuIJLykjUL/OO0PpuGOYMgnLpIvWuQliJpA8wnwLkzd
41+EBia/gWP0WSnaVQIDAQABMA0GCSqGSIb3DQEBCwUAA4IBAQBa8g10CIhVrLlO
f4OkY7lwdPNgGqjqicLdcIx/RskyU42bH++0PwGlVpFcXfwbof3remXHPN2qFpfJ
PWhqJSwJZor7nIshy6WX9mO/dfM0c0vC6zygP/5/1AON+qyWeNu/N+XjglYueca7
/ngi+e2P5S6gOKcbx4A2xYz0YMSLKtldm/PSa+LrQQCTK4cqxFQBdjo1j1X7qC8l
wT7fT4BuDzd89Yb0ehcciOGgTbxPW0XUReq4TKryzvI1E8VbzklLUxQO4UOpQggN
t+CuwmRczSx3sPaMDg34ZR+TmoRWzx9tsHFCIGuPtA7lMdKikQnVzTjX5h2w1snX
2qiz""".strip().replace('\n', '')

    cert_2 = """
MIIDkDCCAngCCQDb0/k1Oex1ODANBgkqhkiG9w0BAQsFADCBiTELMAkGA1UEBhMC
VVMxFjAUBgNVBAgMDU1hc3NhY2h1c2V0dHMxDzANBgNVBAcMBkJvc3RvbjERMA8G
A1UECgwIdGVzdC5jb20xDTALBgNVBAsMBFRFU1QxETAPBgNVBAMMCHRlc3QuY29t
MRwwGgYJKoZIhvcNAQkBFg10ZXN0QHRlc3QuY29tMB4XDTIxMDQxODIxMzg0OVoX
DTIyMDQxODIxMzg0OVowgYkxCzAJBgNVBAYTAlVTMRYwFAYDVQQIDA1NYXNzYWNo
dXNldHRzMQ8wDQYDVQQHDAZCb3N0b24xETAPBgNVBAoMCHRlc3QuY29tMQ0wCwYD
VQQLDARURVNUMREwDwYDVQQDDAh0ZXN0LmNvbTEcMBoGCSqGSIb3DQEJARYNdGVz
dEB0ZXN0LmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALuAknbY
UxccsXCWBiFyUcdGQoiG91k8R9B58nHbrkcVyB2qZkha8fzeNrYfEcvUa9Aor6j8
1mEFHV7abGaxBqb2I10+vNE86B6p75WBxQfvwzlmxbumodTxhHJIbTwDtMSxeSts
OFgp2XQdrtpIEhEF0hAHp4qM7QSbcMsSl+VFm/l9fNKjCGKK5q0Q9umvDBfcnz9p
PeyeqeUKLKBgs8JS6r/FqyNDUgsm0Jxizg0gFi+ot+MGPdCGmHUFcuqblKVSOOgP
27Sc4eNfmZGi5WZb2N/2e8ltZ/7NYolf8OfNsGP0nG4v0KSzDTPjo4IOAWEEsy8V
vs2tbmuQy3nlsFMCAwEAATANBgkqhkiG9w0BAQsFAAOCAQEAh1qchH8lN3bpG4wK
NK03Eavlpptfa2sjklFMamJ0fdP7p7YD5XxI4vHQ8mZumaY473+RKI7Q8Tj8m8ed
SjycG6qyvYEWgBIv5dhcy7TNEebJyup6jjSCvQqWMiA1zmUuCf1YM/SQysZvx97l
yAcIMNkKXDx+jBebXkYfe33iteQCtxsN4ehjUloXONKkLN337uONMBtj+Dqts/e5
4FNdsjhTWuc0e01gahHKhzqdz0J7h1cRkzgu2Ct/JslT5SyFAW356royk65gbgdR
/1hXVqNOV7qKD8ohU3vDPW8Pltvr2hwIOWKo4vykhNG3iXX6hrWKhNESul+kqhVP
5Nwxg==""".strip().replace('\n', '')

    cert_3 = """
MIIDYDCCAkgCCQDOPnykxHJNODANBgkqhkiG9w0BAQsFADByMQswCQYDVQQGEwJV
UzEWMBQGA1UECAwNTWFzc2FjaHVzZXR0czEPMA0GA1UEBwwGQm9zdG9uMRIwEAYD
VQQKDAl0ZXN0My5jb20xEjAQBgNVBAsMCXRlc3QzLmNvbTESMBAGA1UEAwwJdGVz
dDMuY29tMB4XDTIxMDQxODIxMTgwM1oXDTIyMDQxODIxMTgwM1owcjELMAkGA1UE
BhMCVVMxFjAUBgNVBAgMDU1hc3NhY2h1c2V0dHMxDzANBgNVBAcMBkJvc3RvbjES
MBAGA1UECgwJdGVzdDMuY29tMRIwEAYDVQQLDAl0ZXN0My5jb20xEjAQBgNVBAMM
CXRlc3QzLmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALNa/IAg
k1E0S0RDNCn/6DQ1b71y6YuIjpz8Xq3ZUYZiIo3yZ291isAsEVlcg9MH0HQ1TKCh
OybXax0eLF2kmIGSVHdV9zvNmEZ+55xy4Ya1qt+nVmA3UMU3LEynXi2tnXcJa4SP
hrtXEtMKlwNbvg+Cb0PYFCpPOTfOp/DrW8dNHKLaW/kZxyVVVgge4AUw45j+QucM
NHHi/up/J9u7Y87AFBXTtXNf4zMZPUEugaco/oY8u9OzMXs2ffMQP2QfuJKzRjsm
W5aZs3ytj8R6gyvFuPPSi8PJDkXVP/WRvOOB/rSwhPqen9StuEJIVvAn4RYm/dQA
dlqMwWEi24g+q5UCAwEAATANBgkqhkiG9w0BAQsFAAOCAQEAchY+sHcAgKBdgPOX
GFI3/L9u3Hw1ApS9XwOlwqNbEjERISV3xjk8C37GmDPS4rpH1iEehDeKwzNEl7Fa
fEgM5387jdQnCXsaxAkFO4xgb/O9Vpma8Lz5t9QRU62j9ylSObNgXmOSJ9EPJYC/
XL8RejTQW6gNVbH8DzydBvTyUsnpSyNy4uon+PBHUsDuMNomibEIsQUWakntA25D
JN/iQ8IOsRBmnvX3tTtSb7uV9DaEomIhHtiiGfxs3qyyLbZHN1HpKZvKsP4xOwB8
vh0z4HWPD+LLh4XQFn3VIqt4p4QtnzQ0lkzRZaHpbzGcLE6gXTy9ObFZPWQ/sGV/
yE74hA==""".strip().replace('\n', '')

    return {'Certificates': [cert_1, cert_2, cert_3]}
