from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

# import
openai.api_key  = "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"


app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
  return 'Hello, World!'


@app.route("/api/upload", methods=["POST"])
def upload_file():
  file = request.files["file"]
  if file:
    file.save("uploads/" + file.filename)
    return "success"
  else:
    return "failed"

@app.route("/api/llm", methods=["POST"])
def get_completion():
  # 从请求中获取message信息
  prompt = request.form['message']

  # temprary model
  model="gpt-3.5-turbo"
  # send message
  messages = [{"role": "user", "content": prompt}]
  response = openai.ChatCompletion.create(
      model=model,
      messages=messages,
      temperature=0, # this is the degree of randomness of the model's output
  )
  # return response
  return jsonify({"message": response.choices[0].message["content"]})

@app.route("/api/llm2", methods=["POST"])
def get_completion_from_messages(messages):
    # temprary model
    model="gpt-3.5-turbo"
    temperature=0

    # send message
    messages = request.form['messages']
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
#     print(str(response.choices[0].message))
    return jsonify({"message": response.choices[0].message["content"]})



if __name__ == '__main__':
    app.run()

