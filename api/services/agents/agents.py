from langchain_ollama import ChatOllama

from schemas import DefinitionAIOutputSchema, DefinitionsListSchema

import os 
from datetime import datetime
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


ollama_url = os.getenv("OLLAMA_URL")


model = ChatOllama(
    model="qwen2.5",
    temperature=0.2,   # more deterministic, better for definitions
    top_k=40,          # restricts vocabulary sampling = fewer hallucinations
    top_p=0.9,         # prevents overly creative responses
    repeat_penalty=1.05,  # avoids word repetition
    base_url=ollama_url
)

structured_model = model.with_structured_output(DefinitionsListSchema)

def process_word(term: str) -> DefinitionsListSchema:
    msgs = [
        {
            "role": "system",
            "content": (
                "You are a professional language-learning assistant. "
                "Your task is to generate clear, simple definitions for a given word.\n\n"
                
                "Requirements:\n"
                "1. Provide max 3 definitions, ordered from most common to most rare.\n"
                "2. For each definition, provide:\n"
                "   - A simple, easy-to-understand definition.\n"
                f"   - A usage example sentence. IMPORTANT: The example MUST contain the exact word \"{term}\".\n"
                "   - A list of up to 5 synonyms.\n\n"
                
                "Guidelines:\n"
                "- Definitions must be concise and understandable for learners.\n"
                f"- Every example sentence MUST include the word \"{term}\" - this is mandatory.\n"
                "- Only include definitions that are relevant and correct for the word."
            )
        },
        {
            "role": "user",
            "content": f"Generate definitions for the word: {term}"
        }
    ]
    try:
        time_before = datetime.now()
        result: DefinitionsListSchema = structured_model.invoke(msgs) # type: ignore
        time_after = datetime.now()
        elapsed = (time_after - time_before).total_seconds()
        logger.info(f"Processed word '{term}' in {elapsed:.2f} seconds.")
        logger.info(f"Structured result: {result}")
        return result  
    except Exception as e:
        logger.error(f"Error in process_word: {e}", exc_info=True)
        raise

