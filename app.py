from flask import Flask, request, jsonify, Response
import json
from models import GrammarChecker, ModelRefusalError
from pydantic import BaseModel
from openai import OpenAI, LengthFinishReasonError

app = Flask(__name__)


def get_openai_client():
    return OpenAI()


def check_grammar(raw_text: str):
    client = get_openai_client()

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a grammar checker that corrects grammar. "
                    "You inform the user of every sentence where there is a mistake, provide a corrected sentence, "
                    "and point out type of error in a succinct manner. "
                    "In the end you also provide the full corrected text."
                ),
            },
            {"role": "user", "content": raw_text},
        ],
        max_tokens=1000,
        response_format=GrammarChecker,
    )

    grammar_checker = completion.choices[0].message

    if grammar_checker.refusal:
        raise ModelRefusalError(grammar_checker.refusal)

    if grammar_checker.parsed:
        return grammar_checker.parsed.model_dump_json(indent=2)


@app.post("/check-grammar")
def check_grammar_endpoint():
    if request.is_json:
        data = request.get_json()
        raw_text = data.get("raw_text", "")

        if not raw_text:
            return jsonify({"error": "No text provided"}), 400

        try:
            result = check_grammar(raw_text)
            return Response(result, mimetype="application/json"), 200

        except ModelRefusalError as e:
            return (
                jsonify({"error": "Model refused to answer", "refusal_reason": str(e)}),
                400,
            )

        except LengthFinishReasonError as e:
            return (
                jsonify({"error": "Response exceeded token limit"}),
                400,
            )
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"error": "Invalid request format, expected JSON"}), 400


if __name__ == "__main__":
    app.run()
