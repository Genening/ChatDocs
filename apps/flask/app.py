from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
import hashlib

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
    split_name = file.filename.split(".")
    folder = hashlib.md5(split_name[0].encode()).hexdigest()
    # 判断文件夹是否存在
    if not os.path.exists(f"uploads/{folder}"):
      os.mkdir(f"uploads/{folder}")
    file.save(f"uploads/{folder}/" + file.filename)
    return "success"
  else:
    return "failed"


@app.route("/api/getDocList", methods=["GET"])
def get_doc_list():
  return jsonify(os.listdir("uploads"))


@app.route("/api/getFileList", methods=["GET"])
def get_file_list():
  filepath = request.args.get("filepath")
  return jsonify(os.listdir(f"uploads/{filepath}"))


@app.route("/api/getQuestionList", methods=["GET"])
def get_question_list():
  docpath = request.args.get("docpath")
  content = ""
  for file in os.listdir(f"uploads/{docpath}"):
    with open(f"uploads/{docpath}/{file}", "r", encoding="utf-8") as f:
      content += f.read()

  prompt = u"Suggest 3 simple, clear, single, short questions base on the context, answer in the same language of context\n\nContext:"+content+u"\n\nAnswer with the language used in context, please number questions in 1/2/3, and the first line is 'Suggest question: ', strict follow markdown format, end with\\n, questions are:"
  messages = [{"role": "user", "content": prompt}]
  model = "gpt-3.5-turbo"
  temperature = 0
  response = openai.ChatCompletion.create(
    model=model,
    messages=messages,
    temperature=temperature, # this is the degree of randomness of the model's output
  )

  return jsonify(response.choices[0].message["content"])


@app.route("/api/llm", methods=["POST"])
def get_completion():
  # 从请求中获取message信息
  question = request.form['question']
  docpath = request.args.get("docpath")
  content = ""
  for file in os.listdir(f"uploads/{docpath}"):
    with open(f"uploads/{docpath}/{file}", "r", encoding="utf-8") as f:
      content += f.read()

  prompt = u"Question: "+question+u"\n\nContext:"+content+u"\n\nAnswer with the content includes and the language used in context, add some suitable emoji in the answer and encourage user to ask more in the end of answer, the answer is:"

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
