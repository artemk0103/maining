import urllib.request
import hashlib
import random
import json
import time


BASE_URL   = f'http://213.189.53.91:1488'


wallet     = 'doxerpidorcoziestozhe' # Адрес кошелька
difficulty = 6 # Сложность (минимум 5). Чем выше это значение, тем больше приносит майнинг, однако тем больше затраты по времени добычи блока.


uid = random.randint(1_000_000, 9_999_999)


def get_last_block() -> dict:
    data = {
        'uid': uid
    }

    request = urllib.request.Request(f'{BASE_URL}/blockchain/lastBlock', json.dumps(data).encode(), {'Content-Type': 'application/json'}, method='GET')
    response = urllib.request.urlopen(request)
    data = response.read()
    data = json.loads(data.decode('utf-8'))
    return data


def add_block(proof: int, previous_hash: str) -> dict:
    data = {
        'uid': uid,
        'proof': proof,
        'previous_hash': previous_hash,
        'wallet': wallet
    }

    request = urllib.request.Request(f'{BASE_URL}/blockchain/addBlock', json.dumps(data).encode(), {'Content-Type': 'application/json'}, method='POST')
    response = urllib.request.urlopen(request)
    data = response.read()
    data = json.loads(data.decode('utf-8'))

    return data


def new_blockchain() -> None:
    data = {
        'uid': uid
    }

    request = urllib.request.Request(f'{BASE_URL}/blockchain/new', json.dumps(data).encode(), {'Content-Type': 'application/json'}, method='POST')
    urllib.request.urlopen(request)


def hash(block: dict) -> str:
    string = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(string).hexdigest()


def valid_proof(last_proof: int, proof: int, last_hash: str) -> bool:
    guess = f'{last_proof}{proof}{last_hash}'.encode()
    hash = hashlib.sha256(guess).hexdigest()
    return hash[:difficulty] == '0' * difficulty


def proof_of_work(last_block: dict) -> int:
    last_proof = last_block['proof']
    last_hash = hash(last_block)

    proof = 0
    while not valid_proof(last_proof, proof, last_hash):
        proof += 1

    return proof


print('===============')
print('TCMiner v1.0.00')
print('Made by @pwned')
print('===============')


new_blockchain()


while True:
    try:
        last_block = get_last_block()
        print(last_block)
        proof = proof_of_work(last_block)
        phash = hash(last_block)
        result = add_block(proof, phash)
        print(f'{phash} {proof} {result["response"]}')
    except Exception as e:
        print(f'Error {e}. Reconnecting in 5 seconds...')
        time.sleep(5)
