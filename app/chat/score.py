import random
from .redis import client

def random_component_by_score(component_type, component_map):
    if component_type not in ["llm", "retriever", "memory"]:
        return ValueError('Invalid component Type')
    
    score_values = client.hgetall(f"{component_type}_score_value")
    score_counts = client.hgetall(f"{component_type}_score_count")

    names = component_map.keys()

    avg_scores = {}
    for component_name in names:
        score = int(score_values.get(component_name, 1))
        count = int(score_counts.get(component_name, 1))
        avg = score / count
        avg_scores[component_name] = max(avg, 0.1)
            
        #     if component is component_type:
        # else:
        #     return ValueError('Component does not exists')

    print(avg_scores)
    # get the weightage of the right component
    sum_scores = sum(avg_scores.values())
    random_val = random.uniform(0, sum_scores)
    cumulative = 0

    for name, score in avg_scores.items():
        cumulative =+ score
        if random_val <= cumulative:
            return name


def score_conversation(
    conversation_id: str, score: float, llm: str, retriever: str, memory: str
) -> None:
    score = min(max(score, 0), 1)

    client.hincrby("llm_score_value", llm, score)
    client.hincrby("llm_score_count", llm, 1)

    client.hincrby("retriever_score_value", retriever, score)
    client.hincrby("retriever_score_count", retriever, 1)

    client.hincrby("memory_score_value", memory, score)
    client.hincrby("memory_score_count", memory, 1)

    """
    This function interfaces with langfuse to assign a score to a conversation, specified by its ID.
    It creates a new langfuse score utilizing the provided llm, retriever, and memory components.
    The details are encapsulated in JSON format and submitted along with the conversation_id and the score.

    :param conversation_id: The unique identifier for the conversation to be scored.
    :param score: The score assigned to the conversation.
    :param llm: The Language Model component information.
    :param retriever: The Retriever component information.
    :param memory: The Memory component information.

    Example Usage:

    score_conversation('abc123', 0.75, 'llm_info', 'retriever_info', 'memory_info')
    """

    pass


def get_scores():
    """
    Retrieves and organizes scores from the langfuse client for different component types and names.
    The scores are categorized and aggregated in a nested dictionary format where the outer key represents
    the component type and the inner key represents the component name, with each score listed in an array.

    The function accesses the langfuse client's score endpoint to obtain scores.
    If the score name cannot be parsed into JSON, it is skipped.

    :return: A dictionary organized by component type and name, containing arrays of scores.

    Example:

        {
            'llm': {
                'chatopenai-3.5-turbo': [score1, score2],
                'chatopenai-4': [score3, score4]
            },
            'retriever': { 'pinecone_store': [score5, score6] },
            'memory': { 'persist_memory': [score7, score8] }
        }
    """

    pass
