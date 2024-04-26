def get_open_question():
    presentation_data = []

    # Text Description
    text_description = {
        "type": 1,
        "content": """## Open Questions
This final section includes open-ended questions that allow you to express in more detail your thoughts about the factors influencing your trust in the swarm and the impact of different configurations.
""", }
    presentation_data.append(text_description)

    # Text Survey - Trust Factors
    trust_factors = {
        "type": 13,
        "content": {
            "question": """### Trust Factors
Reflecting on the episode, what specific factors influenced your trust in the swarm?""",
            "answer": ""
        }
    }
    presentation_data.append(trust_factors)

    # Text Survey - Configuration Impact
    config_impact = {
        "type": 13,
        "content": {
            "question": """### Configuration Impact
How did the changes in the swarm configuration across different clips affect your level of trust?""",
            "answer": ""
        }
    }
    presentation_data.append(config_impact)

    return presentation_data
