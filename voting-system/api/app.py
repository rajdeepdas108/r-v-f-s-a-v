from flask import Flask, render_template, jsonify, request
from blockchain.src.system_integration import VotingSystem
import base64
import tempfile

app = Flask(__name__)
voting_system = VotingSystem("https://mainnet.infura.io/v3/YOUR_PROJECT_ID")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/register', methods=['POST'])
def register_voter():
    try:
        image_data = request.files['image'].read()
        voter_id = request.form['voter_id']
        public_key = request.form['public_key']
        
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(image_data)
            voting_system.register_voter(voter_id, tmp.name, public_key)
        
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/vote', methods=['POST'])
def submit_vote():
    try:
        image_data = request.files['image'].read()
        voter_id = request.form['voter_id']
        candidate = request.form['candidate']
        
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(image_data)
            tx_hash = voting_system.cast_vote(voter_id, tmp.name, candidate)
        
        return jsonify({
            "status": "success",
            "tx_hash": tx_hash.hex(),
            "merkle_proof": voting_system.merkle.get_proof(0)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/results')
def get_results():
    try:
        results = voting_system.tally_votes()
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)