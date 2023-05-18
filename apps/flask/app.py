from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
import hashlib
from extract_file import get_file_content

# 设置openai的api key
openai.api_key  = "sk-"
# 初始化全局常量
CONTEXT_TOKEN_LIMIT = 1500

# 初始化flask
app = Flask(__name__)
CORS(app)

# 开辟接口
@app.route('/')
def hello():
  return 'Hello, World!'


@app.route("/api/upload", methods=["POST"])
def upload_file():
  docpath = request.args.get("docpath")
  file = request.files["file"]
  if file:
    if docpath and os.path.exists(f"uploads/{docpath}"):
      file.save(f"uploads/{docpath}/" + file.filename)
    else:
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
    filepath = f"uploads/{docpath}/{file}"
    content += get_file_content(filepath)

  # 设置最大长度
  if len(content) > CONTEXT_TOKEN_LIMIT:
    content = content[:CONTEXT_TOKEN_LIMIT]

  prompt = u"Suggest 3 simple, clear, single, short questions base on the context, use same language in the context, \n\nContext:"+content+u"\n\nThe first line of response is 'Suggest question: '. Please number questions in 1/2/3, no need foe answers, strictly follow the markdown format and show the answer clearly, questions are:"
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
    content += get_file_content(f"uploads/{docpath}/{file}")

  # 设置最大长度
  if len(content) > CONTEXT_TOKEN_LIMIT:
    content = content[:CONTEXT_TOKEN_LIMIT]

  prompt = u"Question: "+question+u"\n\nContext:"+content+u"\n\nAnswer with the content includes and the language used in context, please specify the page number relate with answer if there is anyone, add some suitable emojis in the answer and encourage user to ask more in the end of answer, the answer is:"

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
