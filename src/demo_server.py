"""Temporary localhost evidence viewers for recording a reproducible demo; not published."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from server import app
from flask import send_from_directory
@app.get('/demo-proof/<name>')
def demo_proof(name):
 if name not in ['ontology','sources','rdf','endpoint','inference','checks']:return {'error':'Not found'},404
 return send_from_directory(Path(__file__).resolve().parents[1]/'evidence/demo',name+'.html')
if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8002)
 app.run(host='127.0.0.1',port=parser.parse_args().port,debug=False)
