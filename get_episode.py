from typing import List

"""
1. A Caption of the whole video

2. Evaluation by clips: For each clip:

(1) Video Clip {i}: /video_path

(2) Single Options: {From 1 to 5} with Text explanations:
'''
### Trust Score (for this clip only)

After watching this clip, please rate your level of trust to the swarm (a higher score indicating greater trust in the swarm).
'''

3. Overall Evaluations:

(1) Single Options: {From 1 to 5} with Text explanations:
'''
### Trust Score (after all clips)
Considering the entire episode, rate your overall trust in the swarm’s ability to perform the task effectively (a higher score indicating greater trust in the swarm).
'''

(2) Cause of Distrust with Text explanations:
'''
### Distrust Reason (for this clip only, if a fault or distrust is identified)

'''
Multiple Options: {Option 1, Option2 ...}
"""


def get_episode(video_paths: List, k=2, index=1):
    presentation_data = [
        {
            "type": 1,
            "content": "# Title"
        },
        {
            "type": 11,
            "content": {
                "question": """### Trust Score (for this clip only)
After watching this clip, please rate your level of trust to the swarm (a higher score indicating greater trust in the swarm).""",
                "options": ["1", "2", "3", "4", "5"],
                "answer": "2"
            }
        },
        {
            "type": 13,
            "content": {
                "question": "##### Any additional comments for this clip?",
                "answer": "Please enter..."
            }
        },
        # 总体评估的示例内容
        {
            "type": 11,
            "content": {
                "question": """### Overall Trust Rating (after all clips)
Considering the entire episode, rate your overall trust in the swarm’s ability to perform the task effectively (a higher score indicating greater trust in the swarm).""",
                "options": ["1", "2", "3", "4", "5"],
                "answer": "3"
            }
        },
        {
            "type": 12,
            "content": {
                "question": """### Distrust Reason (for this clip only, if a fault or distrust is identified)
If you identified a fault or tend to distrust the swarm, please explain your reason in short.""",
                "options": ["1", "2", "3", "4", "5"],
                "answer": "3"
            }
        }
    ]
    assert len(video_paths) == k
    formatted_content = []

    formatted_content.append({"type": 1, "content": f"""### Evaluations by Clips on Episode {index}
In the videos, the UAV swarm was deployed for search and rescue operations.

Please carefully observe the video and answer the following questions based on your observations of the swarm's search and rescue activities. Feel free to replay the video as needed for validation.
"""})

    for i in range(k):
        formatted_content.append({"type": 1, "content": f"#### Episode {index} - {i + 1}"})
        formatted_content.append({"type": 2, "content": video_paths[i]})
        for j in range(1, 3):
            formatted_content.append(presentation_data[j])
    formatted_content.append({
        "type": 1,
        "content": f"""### Overall Evaluations on Episode {index}
After watching all clips of an episode, this section asks for your overall impressions and trust rating for the entire episode. """}, )
    formatted_content.extend(presentation_data[-2:])
    print(formatted_content)

    return formatted_content