from flask import Flask, jsonify, request
from flask_cors import CORS
from get_episode import get_episode
from get_general import get_open_question

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})

TYPE_MARKDOWN = 1
TYPE_VIDEO = 2
TYPE_SINGLE_CHOICE = 11
TYPE_MULTIPLE_CHOICE = 12
TYPE_TEXT_INPUT = 13

# 测试数据
tutorial_content = [
    {"type": TYPE_MARKDOWN, "content": "# Questionnaire -- Trust Transfer Study in Human-Swarm Interaction"},
    {"type": TYPE_MARKDOWN, "content": """### Project Instruction
Welcome to our research initiative at Cognitive Robotics and AI lab (CRAI) within the College of Aeronautics and Engineering, Kent State University, Ohio, USA. This study is at the forefront of exploring how trust is built, transferred, and maintained in the rapidly evolving field of drone technology.

#### Please refer to the tutorial linked below:
[Tutorial](https://docs.google.com/forms/d/e/1FAIpQLSfnOWGvC3pvSe89fsOHE4kagheAWgB_2WBq0cUpFXZKvLBJeg/viewform)"""},
    # {"type": TYPE_MARKDOWN, "content": "# Tutorial Section 1"},
    # {"type": TYPE_VIDEO, "content": "/test.avi"},
    # {"type": TYPE_VIDEO, "content": "/test.mp4"},
    # {"type": TYPE_VIDEO, "content": "/bags/20240426_013605/output_airsim_video.mp4"},
    # {"type": TYPE_SINGLE_CHOICE,
    #  "content": {"question": "What is the capital of France?", "options": ["Paris", "London", "Berlin"],
    #              "answer": "Paris"}},
]

survey_content = [
    {"type": TYPE_VIDEO, "content": "/bags/20240426_013605/output_airsim_video.mp4"},
    {"type": TYPE_MULTIPLE_CHOICE, "content": {"question": "Which programming languages do you know?",
                                               "options": ["Python", "Java", "JavaScript", "C++"],
                                               "answer": ["Python", "JavaScript"]}},
    {"type": TYPE_TEXT_INPUT,
     "content": {"question": "What is your favorite programming language and why?", "answer": ""}},
]


@app.route('/api/get_tutorial_content', methods=['GET'])
def get_tutorial_content():
    return jsonify(tutorial_content)


@app.route('/api/get_survey_content', methods=['GET'])
def get_survey_content():
    k = 5
    title = "test"
    video_paths = [f"/video/{title}_{i}" for i in range(k)]
    return jsonify(get_episode(video_paths, len(video_paths)))


@app.route('/api/get_general_content', methods=['GET'])
def get_general_content():
    return jsonify(get_open_question())


@app.route('/api/get_content', methods=['GET'])
def get_markdown():
    markdown_content = """Test get_content API"""
    content1 = {"type": TYPE_MARKDOWN, "content": markdown_content}
    video_path = "/bags/20240426_013605/output_airsim_video.mp4"
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
