#python3 -m venv venv
#source venv/bin/activate

pip install -r requirements.txt


curl -X 'POST' \
    'https://llama-3-2-3b-maas-apicast-production.apps.prod.rhoai.rh-aiservices-bu.com:443/v1/completions' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer ' \
    -d '{
    "model": "llama-3-2-3b",
    "prompt": "San Francisco is a",
    "max_tokens": 15,
    "temperature": 0
}'


curl -X 'GET' \
  'https://granite-33-2b-instruct1-maas-apicast-production.apps.cluster-2j5v9.2j5v9.sandbox3159.opentlc.com:443/v1/models' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer '