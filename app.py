from flask import Flask, request, jsonify
import os
import json
from git import Repo

app = Flask(__name__)

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_URL = f"https://{GITHUB_TOKEN}@github.com/DanielSilva22/cristal-semantique-core1.git"
LOCAL_REPO = "/tmp/repo"

@app.route("/push", methods=["POST"])
def push_to_github():
    content = request.json
    path = content.get("path")
    data = content.get("data")

    if not path or data is None:
        return jsonify({"error": "path and data are required"}), 400

    if not os.path.exists(LOCAL_REPO):
        Repo.clone_from(REPO_URL, LOCAL_REPO)

    full_path = os.path.join(LOCAL_REPO, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(data if isinstance(data, str) else json.dumps(data, indent=2, ensure_ascii=False))

    repo = Repo(LOCAL_REPO)
    repo.git.add(path)
    repo.index.commit(f"Auto-push depuis Worker pour {path}")
    origin = repo.remote(name="origin")
    origin.push()

    return jsonify({"status": "success", "path": path})
    
    if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

