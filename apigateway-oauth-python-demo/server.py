from bottle import route, run, request
import python_jwt as jwt, jwcrypto.jwk as jwk, datetime

def get_file_content(file):
    f=open(file)
    content = f.read()
    return content

@route('/check')
def check():
    token = request.headers.get('token')
    pub_pem=str(get_file_content('public_pem')).encode('utf-8')
    pub_key = jwk.JWK.from_pem(pub_pem)
    headers, claims = jwt.verify_jwt(jwt=token, pub_key=pub_key, allowed_algs=['RS256'])
    print(headers)
    print(claims)
    return token
    

@route('/token')
def hello():
    priv_pem=str(get_file_content('priv_pem')).encode('utf-8')
    payload = {'foo': 'bar', 'wup': 90 }
    priv_key = jwk.JWK.from_pem(priv_pem)
    token = jwt.generate_jwt(claims=payload, priv_key=priv_key, algorithm='RS256', lifetime=datetime.timedelta(minutes=5))
    return token

@route('/code')
def code():
    # todo   produce the code
    return "123456"

run(host='0.0.0.0', port=8080, debug=True)

