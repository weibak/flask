
import os
import redis

from flask import Flask, request, render_template

app = Flask(__name__)

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_client = redis.Redis(host=redis_host, port=6379, db=0)


@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        value = None
        if "key" in request.values:
            value = request.values.get("key")
            redis_client.set("key", value)
    else:
        value = redis_client.get("key")
    return render_template("index.html", value=value)


if __name__ == "__main__":
    app.run(host="0.0.0.0")