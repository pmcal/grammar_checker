
# Grammar Checker 

## Table of Contents
1. [Running the code](#running-the-code)
2. [Design Choices](#design-choices)
3. [Challenges Faced](#challenges-faced)
4. [Future Improvements](#future-improvements)

---

## Running the code

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (was not sure if you needed my API key, if so please just ask)

### Installation

1. **Create a virtual environment** :

   \`\`\`bash
   python3 -m venv venv
   source venv/bin/activate
   \`\`\`

2. **Install dependencies**:

   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

   This will install the necessary libraries, including Flask, Pydantic, and OpenAI.

3. **Set your OpenAI API key as an environment variable**:


    Set your OpenAI API key as an environment variable:

   \`\`\`bash
    export OPENAI_API_KEY=your-api-key-here
    \`\`\`

    It was unclear to me if you needed my own API key, if so please just ask.


4. **Run the Flask app**:

   \`\`\`bash
   flask run
   \`\`\`

   The app should now be running at \`http://127.0.0.1:5000\`.


5. **Make POST request using script, or directly**

   You can access the endpoint in one of two ways. The first way is by running a little helper script I wrote, the second way is to just make the post request directly.

   - **Using `check_grammar.sh` script**:

     1. Ensure the Flask app is running (`flask run`).
     2. On a separate shell, run the script by passing the input JSON file and specifying an output file:

     ```bash
     ./check_grammar.sh input.json output.json
     ```

     This will send a POST request to the `/check-grammar` endpoint with the content from `input.json` and store the API response in `output.json`.
    
    - **Making a POST request directly via `curl`**:

     If you prefer to make the request manually, you can use the following `curl` command:

     ```bash
     curl -X POST http://127.0.0.1:5000/check-grammar        -H "Content-Type: application/json"        -d @input.json -o output.json
     ```

     This will send the contents of `input.json` to the API and save the response in `output.json`.


--- 

## **Examples**:

    I have included three examples in this repo. Let's have a look at one in the readme:

     ```bash
     ./check_grammar.sh example_input1.json example_output1.json
     ```

     In this case, the input file contains the following:

     ```json
        {
            "raw_text": "HEllo, my name Is Pedro. Im from portugal and been very happy in Germnany"
        }
     ```

     The output was written to `example_output1.json` with the corrected text and error details.
     In this instance, `example_output1.json` looks like this:

     ```json
        {
        "modifications": [
            {
            "wrong_sentence": "HEllo, my name Is Pedro.",
            "corrected_sentence": "Hello, my name is Pedro.",
            "type_of_error": "Capitalization error"
            },
            {
            "wrong_sentence": "Im from portugal and been very happy in Germnany",
            "corrected_sentence": "I'm from Portugal and have been very happy in Germany.",
            "type_of_error": "Contraction error and tense error"
            }
        ],
        "full_corrected_text": "Hello, my name is Pedro. I'm from Portugal and have been very happy in Germany."
        }
    ```

    The second example is also short, while the third contains a longer paragraph full of errors. Their
    output files can also be found in this repo.



---

## **Design Choices**

- Used Flask for minimalistic backend design.
- Used Openai's model gpt-4o-2024-08-06 for grammar checking. This has several advantages: the model itself is very powerful, and it allows me to make use of the 'structured ouput' feature and system prompts. It's also the framework I'm most accostumed to.


## **Challenges Faced**

- Handling API refusals and exceptions (including exceeding token limits) in a consistent and well organized manner.

- Learning how to use the 'structured ouput' feature of OpenAI API.

- Ensuring consistent JSON responses, with a well established order.

---

## **Future Improvements**

- Asynchronous request handling: right now long-running requests to the OpenAI API can block the server. Ultimately one would want to introduce async requests or a task queue (e.g. Celery) to allow the app to withstand heavier loads

- Rate Limiting: To improve performance and prevent abuse, I would add rate limiting. 

- Add a caching layer (e.g., Redis), in case the user sends repeated requests with the same text.

- More robust error handling: checking the raw_text itself for weird or malformed inputs, etc.

- Adding tests: implement a bunch of tests where the different gramatical errors are isolated. For example, a test for capitalization, another for wrong conjugation, etc. With unambiguous sentences as examples (like "i am pedro" to "I am Pedro") one could cover the basis of most gramatical errors.

- Test out different models: I used the best model, but how different would it be if I use gpt-4o-mini instead? The model is cheaper, would be good to know if the performance changes at all.

---
