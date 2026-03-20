"""
Создание нескольких версий промптов в MLflow Prompt Storage.
Запуск: MLflow должен быть запущен (http://localhost:5000)
  python scripts/create_prompts.py
"""
import mlflow

MLFLOW_TRACKING_URI = "http://localhost:5001"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)


def create_prompts():
    """Создаёт несколько промптов и версий в MLflow Prompt Registry."""

    # Промпт 1: summarization-prompt (версия 1)
    prompt1_v1 = mlflow.genai.register_prompt(
        name="summarization-prompt",
        template="""Summarize content you are provided with in {{ num_sentences }} sentences.

Sentences: {{ sentences }}""",
        commit_message="Initial commit - basic summarization",
        tags={"task": "summarization", "language": "en"},
    )
    print(f"Created: {prompt1_v1.name} version {prompt1_v1.version}")

    # Промпт 1: summarization-prompt (версия 2)
    prompt1_v2 = mlflow.genai.register_prompt(
        name="summarization-prompt",
        template="""You are an expert summarizer. Condense the following content into exactly {{ num_sentences }} clear and informative sentences.

Sentences: {{ sentences }}

Your summary should:
- Contain exactly {{ num_sentences }} sentences
- Include only the most important information
- Be written in a neutral, objective tone""",
        commit_message="Improved - added expert persona and guidelines",
        tags={"task": "summarization", "language": "en"},
    )
    print(f"Created: {prompt1_v2.name} version {prompt1_v2.version}")

    # Промпт 2: classification-prompt (версия 1)
    prompt2 = mlflow.genai.register_prompt(
        name="classification-prompt",
        template="""Classify the following text into one of these categories: {{ categories }}

Text: {{ text }}

Return only the category name.""",
        commit_message="Initial commit - text classification",
        tags={"task": "classification", "language": "en"},
    )
    print(f"Created: {prompt2.name} version {prompt2.version}")

    # Промпт 2: classification-prompt (версия 2)
    prompt2_v2 = mlflow.genai.register_prompt(
        name="classification-prompt",
        template="""You are a classification expert. Analyze the text and assign it to the most appropriate category.

Categories: {{ categories }}

Text to classify: {{ text }}

Instructions:
- Consider the full context of the text
- Return only the exact category name from the list
- If uncertain, choose the best fit""",
        commit_message="Enhanced with expert instructions",
        tags={"task": "classification", "language": "en"},
    )
    print(f"Created: {prompt2_v2.name} version {prompt2_v2.version}")

    # Промпт 3: translation-prompt
    prompt3 = mlflow.genai.register_prompt(
        name="translation-prompt",
        template="""Translate the following text from {{ source_lang }} to {{ target_lang }}.

Text: {{ text }}

Maintain the original tone and style.""",
        commit_message="Initial commit - translation",
        tags={"task": "translation", "language": "multilingual"},
    )
    print(f"Created: {prompt3.name} version {prompt3.version}")

    print("\nDone! Check MLflow UI -> Prompts tab: http://localhost:5001")


if __name__ == "__main__":
    create_prompts()
