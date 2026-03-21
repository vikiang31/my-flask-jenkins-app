from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
      <head>
        <title>My Flask Jenkins App</title>
      </head>
      <body>
        <h1>Hello from Viki's Flask app!</h1>
        <p>This app is tested and built with Jenkins and Docker.</p>
      </body>
    </html>
    """

@app.route("/health")
def health():
    return {"status": "ok"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)