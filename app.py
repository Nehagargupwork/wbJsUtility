# app.py
from flask import Flask, request, jsonify
from keywordRank import get_keyword_rank_and_volume

app = Flask(__name__)

@app.route('/rank', methods=['GET'])
def rank():
    keyword = request.args.get('keyword')
    domain = request.args.get('domain')
    region = request.args.get('region', 'in')
    rank = get_keyword_rank_and_volume(keyword, domain, region)
    return jsonify({'rank': rank})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
