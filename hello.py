import os.path

from flask import Flask, jsonify, request
from flask_cors import CORS
from get_episode import get_episode
from get_general import get_open_question

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})

k = 5
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
    # {"type": TYPE_VIDEO, "content": "/bags/20240426_013605/output_airsim_video.mp4"},
    # {"type": TYPE_SINGLE_CHOICE,
    #  "content": {"question": "What is the capital of France?", "options": ["Paris", "London", "Berlin"],
    #              "answer": "Paris"}},
]

episode_index_num = 1
video_root_dir = "/videos"
video_root_dir_real = os.path.join("./vue-markdown-app/public", video_root_dir.lstrip("/"))


def get_episode_index_num():
    global episode_index_num
    # episode_index_num += 1
    return episode_index_num


def get_titles_mapping():
    print(video_root_dir_real)
    video_files = [f for f in os.listdir(video_root_dir_real) if ".mp4" in f and "__" in f]
    video_titles = [video_file.split("__")[0] for video_file in video_files]
    video_titles = set(video_titles)
    return list(video_titles)


@app.route('/api/get_tutorial_content', methods=['GET'])
def get_tutorial_content():
    return jsonify(tutorial_content)


@app.route('/api/get_survey_content', methods=['GET'])
def get_survey_content():
    global k
    episode_index = get_episode_index_num()
    titles_mapping = get_titles_mapping()
    title = titles_mapping[episode_index]
    video_paths = [os.path.join(video_root_dir, f"{title}__{i}.mp4") for i in range(k)]
    return jsonify(get_episode(video_paths, len(video_paths), index=episode_index))


@app.route('/api/get_general_content', methods=['GET'])
def get_general_content():
    return jsonify(get_open_question())


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
