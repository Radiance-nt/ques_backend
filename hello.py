import os.path

from flask import Flask, jsonify, request
from flask_cors import CORS
from get_episode import get_episode
from get_general import get_open_question
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)
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
]

video_root_dir = "/videos"
video_root_dir_real = os.path.join("./vue-markdown-app/public", video_root_dir.lstrip("/"))


def get_titles_mapping():
    print(video_root_dir_real)
    video_files = [f for f in os.listdir(video_root_dir_real) if ".mp4" in f and "__" in f]
    video_titles = [video_file.split("__")[0] for video_file in video_files]
    video_titles = set(video_titles)
    return list(video_titles)


@app.route('/api/get_tutorial_content', methods=['POST'])
def get_tutorial_content():
    return jsonify(tutorial_content)


@app.route('/api/get_survey_content', methods=['POST'])
def get_survey_content():
    global k
    data = request.get_json()
    username = data.get('username')

    episode_index = get_episode_index_num(username)
    titles_mapping = get_titles_mapping()
    if episode_index >= len(titles_mapping):
        return jsonify({"type": TYPE_MARKDOWN, "content": "# Thank you, you've finished all evaluations!"})
    title = titles_mapping[episode_index]
    video_paths = [os.path.join(video_root_dir, f"{title}__{i}.mp4") for i in range(k)]
    return jsonify(get_episode(video_paths, len(video_paths), index=episode_index))


@app.route('/api/get_general_content', methods=['POST'])
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


@app.route('/api/submit_results', methods=['POST'])
def submit_results():
    data = request.get_json()
    username = data.get('username')
    mode = data.get('username')
    user_answers = [item for item in data['results'] if
                    item['type'] in [TYPE_SINGLE_CHOICE, TYPE_MULTIPLE_CHOICE, TYPE_TEXT_INPUT]]
    if has_user(username):
        create_user(username)

    if mode == "/general":
        err = handle_open_question(user_answers, username)
    elif mode == "survey":
        err = handle_survey(user_answers, username)
    else:
        err = "Unknown mode"
    return jsonify({"success": err is not None, "message": err}), 200


@app.route('/api/bubble', methods=['POST'])
def bubble():
    data = request.get_json()
    username = data.get('username')
    message = f"Survey Finished: {get_episode_index_num(username)},    Open Question: Unfinished"

    return jsonify({"message": message})


def create_user(username):
    users = mongo.db.users
    user_data = {"username": username, "survey": {}, "open_question": {}}
    result = users.insert_one(user_data)
    return result.inserted_id


def has_user(username):
    users = mongo.db.users
    return users.find_one({"username": username}) is not None


def handle_open_question(user_answers, username):
    users = mongo.db.users
    try:
        users.update_one({"username": username}, {"$set": {"open_question": user_answers}})
        return None
    except Exception as e:
        return str(e)


def handle_survey(user_answers, username):
    users = mongo.db.users
    try:
        users.update_one({"username": username}, {"$set": {"survey": user_answers}})
        return None
    except Exception as e:
        return str(e)


def get_episode_index_num(username):
    users = mongo.db.users
    if has_user(username):
        create_user(username)
    user = users.find_one({"username": username})
    if user and "survey" in user:
        return len(user["survey"])
    return 0


if __name__ == '__main__':
    app.run(debug=True)
