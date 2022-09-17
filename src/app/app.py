from flask import Flask
from flask import request
from models.wallet import Wallet
from models.transaction import Transaction, TransactionAddressIndex
import time
from services.blockchain import get_single_address_info
import json
from flask import Response
from flask import jsonify
import threading

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/api/add_btc_address', methods=['POST'])
def add_btc_address():
    address: str = request.json.get('address')
    wallet_item = Wallet(address=address, balance=0, last_updated_ms=_get_time_now_ms(), is_updating=True)
    wallet_item.save()
    _sync(address)

    return Response(status=200)

@app.route('/api/remove_btc_address', methods=['POST'])
def remove_btc_address():
    address: str = request.json.get('address')
    try:
        wallet_item = Wallet.get(address)
    except:
        return Response(status=404)
    
    wallet_item.delete()
    return Response(status=200)

@app.route('/api/sync_wallet', methods=['POST'])
def sync_wallet():
    address: str = request.json.get('address')
    try:
       Wallet.get(address)
    except:
        return Response(status=404)
    
    background_sync(address)
    
    return Response(status=200)

@app.route('/api/balance', methods=['GET'])
def balance():
    address: str = request.json.get('address')
    try:
       wallet_item = Wallet.get(address)
    except:
        return Response(status=404)
    
    if wallet_item.is_updating:
        return Response(status=204)

    return jsonify(wallet_item.balance)

@app.route('/api/transactions', methods=['GET'])
def transactions():
    address: str = request.json.get('address')
    limit: int = request.json.get('limit', 5)
    last_key: str = request.json.get('last_key')
    try:
       wallet_item = Wallet.get(address)
    except:
        return Response(status=404)
    
    if wallet_item.is_updating:
        return Response(status=204)

    txs = TransactionAddressIndex.query(address, last_evaluated_key=last_key, limit=limit)
    txs_list = list(txs)
    txs_dict = {}
    for tx in txs_list:
        txs_dict[tx.tx_id] = tx.tx_details
    response = {
        'txs': txs_dict,
        'last_key': txs.last_evaluated_key
    }

    return jsonify(response)

def _get_time_now_ms():
    return time.time() * 1000 // 1

def background_sync(address):
    t = threading.Thread(target=_sync, args=(address,))
    t.start()

def _sync(address: str):
    address_data = get_single_address_info(address)
    balance = address_data['final_balance']
    txs = address_data['txs']
    count = 0
    wallet_item = Wallet.get(address)
    wallet_item.update(actions=[
        Wallet.is_updating.set(True)
    ])
     # only write 10 items at the time to avoid throttling
    for tx in txs:
        tx_item = Transaction(tx_id=tx['hash'], tx_created_at_ms=tx['time'], tx_details=json.dumps(tx), address=address)
        tx_item.save()
        time.sleep(0.1)
        count += 1
        if count == 10:
            break
        
    wallet_item.update(actions=[
        Wallet.balance.set(balance),
        Wallet.last_updated_ms.set(_get_time_now_ms()),
        Wallet.is_updating.set(False)
    ])

def _create_tables():
    if not Wallet.exists():
        Wallet.create_table()
    if not Transaction.exists():
        Transaction.create_table()

def _delete_tables():
    Wallet.delete_table()
    Transaction.delete_table()

if __name__ == "__main__":
    _create_tables()
    app.run(debug=True, host='0.0.0.0', port=5001)
