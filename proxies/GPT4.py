from openai import OpenAI
import json
from google.colab import userdata

def read_text_GPT4(base64_image):
    api_key = userdata.get('OPENAI_API_KEY')
    
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model='gpt-4-vision-preview', 
        messages=[
          {
            "role": "user",
            "content": [
                {"type": "text", "text": "Your goal is to read ALL the text in the provided image."},
                {"type": "text", "text": "Return JSON document with data. Only return JSON not other text. Avoid newlines and any text that is not pure JSON. If the document contains sections and subsections please clearly describe them. Do not try to read text inside images. Keep the original language. Try to structure the response using the following hierarchy: Main Title > Chapter > Paragraph. Use the following JSON as a template: {\"documentTitle\":\"The Title of the Document\",\"chapters\":[{\"chapterTitle\":\"Chapter 1\",\"sections\":[{\"sectionTitle\":\"Section 1.1\",\"sectionContent\":\"Content of Section 1.1.\"},{\"sectionTitle\":\"Section 1.2\",\"sectionContent\":\"Content of Section 1.2.\"}]},{\"chapterTitle\":\"Chapter 2\",\"sections\":[{\"sectionTitle\":\"Section 2.1\",\"sectionContent\":\"Content of Section 2.1.\"},{\"sectionTitle\":\"Section 2.2\",\"sectionContent\":\"Content of Section 2.2.\"},{\"sectionTitle\":\"Section 2.3\",\"sectionContent\":\"Content of Section 2.3.\"}]}]}"},
                #{"type": "text", "text": "If the image contains partial pages ignore them and all the text in them."},
                {"type": "text", "text": "Break the text into different sections only if there is a very clear reason for it like a new line and an indentation on the new line. In case of doubt, do not create a new section and keep the text in the same section."},
                {"type": "text", "text": "Try your best to read all the text in the image. Do not leave anything out."},
                {"type": "text", "text": "Before sending the response validate the JSON and fix it in case it is not a valid JSON."},
                {
                    "type": "image_url",
                    "image_url": {
                      "url": f"data:image/png;base64,{base64_image}"
                    }
                }
            ],
          }
        ],
        max_tokens=4096,
    )

    json_string = response.choices[0].message.content
    json_string = json_string.replace("json\n", "").replace("\n", "").replace("```", "")

    try:
      jsonObj = json.loads(json_string)
      json_string = json.dumps(jsonObj, indent=4)
    finally: 
      return json_string

def get_text_boxes_GPT4(base64_image):
    api_key = userdata.get('OPENAI_API_KEY')
    
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model='gpt-4-vision-preview', 
        messages=[
          {
            "role": "user",
            "content": [
                {"type": "text", "text": "Your goal is to find the text areas inside the image and define their bounding boxes. The image contains a page of text."},
                {"type": "text", "text": "The output must be an array of all the image areas containing text and text only. Cut away any area without a text."},
                {"type": "text", "text": "Each area should contain a coherent block of text. A chapter, a paragraph or a single block of notes, for example."},
                {"type": "text", "text": "The areas you are creating must not overlap each other"},
                {"type": "text", "text": "Each area is defined by the coordinates of its left-upper corner and its righ-bottom corner, pixelwise. Use the upper-left corner of the image as the (0,0) coordinate."},
                {"type": "text", "text": "Return JSON document with data. Only return JSON not other text. Avoid newlines and any text that is not pure JSON. Use the following JSON as a template: {\"text-boxes\":[{\"id\":\"1\",\"left_upper\":{\"x\":1,\"y\":5},\"right_bottom\":{\"x\":4,\"y\":2}},{\"id\":\"2\",\"left_upper\":{\"x\":2,\"y\":6},\"right_bottom\":{\"x\":5,\"y\":3}},{\"id\":\"3\",\"left_upper\":{\"x\":3,\"y\":7},\"right_bottom\":{\"x\":6,\"y\":4}}]}."},
                {"type": "text", "text": "Before sending the response validate the JSON and fix it in case it is not a valid JSON."},
                {
                    "type": "image_url",
                    "image_url": {
                      "url": f"data:image/png;base64,{base64_image}"
                    }
                }
            ],
          }
        ],
        max_tokens=4096,
    )

    json_string = response.choices[0].message.content
    json_string = json_string.replace("json\n", "").replace("\n", "").replace("```", "")

    try:
      jsonObj = json.loads(json_string)
      json_string = json.dumps(jsonObj, indent=4)
    finally: 
      return json_string