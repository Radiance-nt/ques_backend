from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})

TYPE_MARKDOWN = 1
TYPE_VIDEO = 2


@app.route('/api/get_content', methods=['GET'])
def get_markdown():
    markdown_content = """# Hello Markdown!
This is a simple markdown example:
- List item 1
- List item 2
- List item 3

"""
    content1 = {"type": TYPE_MARKDOWN, "content": markdown_content}
    video_path = "/home/radiance/projects/Swarm-Formation/bags/20240426_013605"
    content2 = {"type": TYPE_VIDEO, "content": video_path}
    # return jsonify([content1, content2])
    return jsonify(content1)


if __name__ == '__main__':
    app.run(debug=True)
