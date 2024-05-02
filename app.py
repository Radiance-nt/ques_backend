import os.path
import random

from flask import Flask, jsonify, request
from flask_cors import CORS
from get_episode import get_episode
from get_general import get_open_question
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)
CORS(app, resources={r"/*": {"origins": "*"}})

k = 5
TYPE_MARKDOWN = 1
TYPE_VIDEO = 2
TYPE_SINGLE_CHOICE = 11
TYPE_MULTIPLE_CHOICE = 12
TYPE_TEXT_INPUT = 13
TYPE_SUBMIT_BUTTON = 99

tutorial_content = [
    {"type": TYPE_MARKDOWN, "content": "# Questionnaire -- Trust Transfer Study in Human-Swarm Interaction"},
    {"type": TYPE_MARKDOWN, "content": """### Project Instruction
Welcome to our research initiative at Cognitive Robotics and AI lab (CRAI) within the College of Aeronautics and Engineering, Kent State University, Ohio, USA. This study is at the forefront of exploring how trust is built, transferred, and maintained in the rapidly evolving field of drone technology.

#### Please refer to the tutorial linked below:
[Tutorial](https://docs.google.com/forms/d/e/1FAIpQLSfnOWGvC3pvSe89fsOHE4kagheAWgB_2WBq0cUpFXZKvLBJeg/viewform)"""},
]

video_root_dir = "/videos"
video_root_dir_real = os.path.join("./vue-markdown-app/public", video_root_dir.lstrip("/"))


def get_all_video_titles():
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
    data = request.get_json()
    username = data.get('username')
    episode_index = get_episode_index_num(username)

    user_doc = mongo.db.users.find_one({"username": username})
    next_video = user_doc.get("next_survey", None)
    if not next_video:
        all_videos = set(get_all_video_titles())
        completed_videos = get_completed_episodes(username)

        available_videos = list(all_videos - completed_videos)
        if not available_videos:
            return jsonify({"type": TYPE_MARKDOWN, "content": "# Thank you, you've finished all evaluations!"})

        next_video = random.choice(available_videos)
        mongo.db.users.update_one({"username": username}, {"$set": {"next_survey": next_video}})

    video_paths = [os.path.join(video_root_dir, f"{next_video}__{i}.mp4") for i in range(k)]
    results = get_episode(video_paths, len(video_paths), index=episode_index)
    results.append({"type": TYPE_SUBMIT_BUTTON, "content": "Submit Results"})
    return jsonify(results)


@app.route('/api/get_general_content', methods=['POST'])
def get_general_content():
    data = request.get_json()
    username = data.get('username')
    open_questions = get_open_question()
    _ = get_episode_index_num(username)
    users = mongo.db.users
    user = users.find_one({"username": username})
    if user and "open_question" in user and user["open_question"]:
        user_answers = user["open_question"]
        for question in open_questions:
            if question['type'] in [TYPE_SINGLE_CHOICE, TYPE_MULTIPLE_CHOICE, TYPE_TEXT_INPUT]:
                if 'question' in question['content']:
                    question_text = question['content']['question']
                    for answer in user_answers:
                        if answer['content']['question'] == question_text:
                            question['content']['answer'] = answer['content'].get('answer', '')
    open_questions.append({"type": TYPE_SUBMIT_BUTTON, "content": "Submit Results"})
    return jsonify(open_questions)


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
    mode = data.get('mode')
    user_answers = [item for item in data['results'] if
                    item['type'] in [TYPE_SINGLE_CHOICE, TYPE_MULTIPLE_CHOICE, TYPE_TEXT_INPUT]]
    if not has_user(username):
        create_user(username)

    if "general" in mode:
        err = handle_open_question(user_answers, username)
    elif "survey" in mode:
        err = handle_survey(user_answers, username)
    else:
        err = "Unknown mode"
        return jsonify({"success": err is not None, "message": err}), 500

    return jsonify({"success": err is not None, "message": err}), 200


@app.route('/api/bubble', methods=['POST'])
def bubble():
    data = request.get_json()
    username = data.get('username')
    if username == "Guest" or username is None:
        return jsonify({"message": "Please login first to see your status."})

    episode_index = get_episode_index_num(username)

    users = mongo.db.users
    user = users.find_one({"username": username})
    open_question_status = "Finished" if user and "open_question" in user and user["open_question"] else "Unfinished"

    message = f"Survey Finished: {episode_index},    Open Question: {open_question_status}"

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
    user = users.find_one({"username": username})
    episode = user.get("next_survey")
    if not episode:
        return "No active survey episode"
    try:
        users.update_one({"username": username}, {"$addToSet": {f"survey.{episode}": user_answers}})
        mongo.db.users.update_one({"username": username}, {"$set": {"next_survey": None}})
        return None
    except Exception as e:
        return str(e)


# Retrieve the number of completed episodes
def get_completed_episodes(username):
    users = mongo.db.users
    user = users.find_one({"username": username})
    if user and "survey" in user:
        return set(user["survey"].keys())
    return set()


def get_episode_index_num(username):
    users = mongo.db.users
    if not has_user(username):
        create_user(username)
    user = users.find_one({"username": username})
    if user and "survey" in user:
        return len(user["survey"])
    return 0


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8081)
