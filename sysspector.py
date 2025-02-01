import graphene 
from flask import Flask, request, jsonify
from flask_graphql import GraphQLView
from sklearn.ensemble import IsolationForest
import numpy as np
import click
import requests
import os
from functools import wraps

API_KEY = os.getenv("API_KEY", "default-secure-key")  

def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if auth_header != f"Bearer {API_KEY}":
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function

class RealTimeAnalysis:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1)

    def train(self, data):
        self.model.fit(data)

    def analyze(self, data):
        prediction = self.model.predict(data)
        return "Anomaly" if prediction[0] == -1 else "Normal"

def anonymize_data(data):
    # Anonymization, e.g., replacing values ​​with generic representations
    if isinstance(data, np.ndarray):
        return np.array([0.0 if x > 0.5 else 1.0 for x in data[0]])
    return data

class SystemInfo(graphene.ObjectType):
    docker = graphene.String()
    ip = graphene.String()
    hostname = graphene.String()

class AnalysisResult(graphene.ObjectType):
    prediction = graphene.String()
    confidence = graphene.Float()

class Query(graphene.ObjectType):
    get_system_info = graphene.Field(SystemInfo)
    analyze_system_info = graphene.Field(AnalysisResult)

    def resolve_get_system_info(self, info):

      return SystemInfo(docker="Docker Info", ip="192.168.1.1", hostname="localhost")

    def resolve_analyze_system_info(self, info):
        analysis = RealTimeAnalysis()
        data = np.random.rand(1, 3)  # Dados de exemplo para análise
        anonymized_data = anonymize_data(data)  # Anonimização dos dados
        prediction = analysis.analyze(anonymized_data)
        return AnalysisResult(prediction=prediction, confidence=0.95)

schema = graphene.Schema(query=Query)

app = Flask(__name__)
app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route("/protected", methods=["GET"])
@authenticate
def protected_route():
    return jsonify({"message": "You are authenticated"}), 200

@click.group()
def cli():
    pass

@cli.command()
@click.option("--system", help="System ID to analyze")
def analyze(system):
    query = """
    {
        analyzeSystemInfo {
            prediction
            confidence
        }
    }
    """
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.post("http://localhost:8000/graphql", json={"query": query}, headers=headers)
    result = response.json()
    click.echo(f"Analysis Result: {result}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="SysSpector Application")
    parser.add_argument("--mode", choices=["api", "cli"], required=True, help="Mode to run the application")
    args = parser.parse_args()

    if args.mode == "api":
        app.run(host="0.0.0.0", port=8000, ssl_context="adhoc")  
    elif args.mode == "cli":
        cli()
