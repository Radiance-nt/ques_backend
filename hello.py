from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})

TYPE_MARKDOWN = 1
TYPE_VIDEO = 2
TYPE_SINGLE_CHOICE = 11
TYPE_MULTIPLE_CHOICE = 12
TYPE_TEXT_INPUT = 13

# 测试数据
tutorial_content = [
    {"type": TYPE_MARKDOWN, "content": "# Tutorial Section 1"},
    {"type": TYPE_VIDEO, "content": "/home/radiance/projects/Swarm-Formation/bags/20240426_013605/output_airsim_video.mp4"},
    {"type": TYPE_SINGLE_CHOICE,
     "content": {"question": "What is the capital of France?", "options": ["Paris", "London", "Berlin"],
                 "answer": "Paris"}},
]

survey_content = [
    {"type": TYPE_VIDEO, "content": "/home/radiance/projects/Swarm-Formation/bags/20240426_013605/output_airsim_video.mp4"},
    {"type": TYPE_MULTIPLE_CHOICE, "content": {"question": "Which programming languages do you know?",
                                               "options": ["Python", "Java", "JavaScript", "C++"],
                                               "answer": ["Python", "JavaScript"]}},
    {"type": TYPE_TEXT_INPUT,
     "content": {"question": "What is your favorite programming language and why?", "answer": ""}},
]

general_content = [
    {"type": TYPE_TEXT_INPUT,
     "content": {"question": "Do you have any feedback or suggestions for this survey?", "answer": ""}},
]


@app.route('/api/get_tutorial_content', methods=['GET'])
def get_tutorial_content():
    return jsonify(tutorial_content)


@app.route('/api/get_survey_content', methods=['GET'])
def get_survey_content():
    return jsonify(survey_content)


@app.route('/api/get_general_content', methods=['GET'])
def get_general_content():
    return jsonify(general_content)


@app.route('/api/get_content', methods=['GET'])
def get_markdown():
    markdown_content = """Test get_content API"""
    content1 = {"type": TYPE_MARKDOWN, "content": markdown_content}
    video_path = "/home/radiance/projects/Swarm-Formation/bags/20240426_013605/output_airsim_video.mp4"
    content2 = {"type": TYPE_VIDEO, "content": video_path}
    return jsonify([content1, content2])


@app.route('/api/direct', methods=['POST'])
def direct():
    data = request.json
    button_number = data.get('buttonNumber')

    if button_number == 1:
        return jsonify({"redirectUrl": "/tutorial"})
    elif button_number == 2:
        return jsonify({"redirectUrl": "/survey"})
    elif button_number == 3:
        return jsonify({"redirectUrl": "/general"})
    else:
        return jsonify({"redirectUrl": "/"})


if __name__ == '__main__':
    app.run(debug=True)
