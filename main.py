import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# [수정됨] Render 금고(환경 변수)에서 키를 가져오도록 설정
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/generate-story', methods=['POST'])
def generate_story():
    data = request.json
    subject = data.get('subject', '')
    
    prompt = f"당신은 노벨 문학상 후보에 오를 법한 모든 분야에 통달한 천재 현대 소설가입니다. 다음 주제를 바탕으로 깊이 있는 은유와 세밀한 심리 묘사가 담긴 단편 소설을 작성하세요. 주제: {subject} 에 대해 문학적인 소설을 한 문단 작성하세요. [작성 규칙]
    1. 독자의 상상력을 자극하는 문학적인 문체를 사용할 것.
    2. 사건 중심이 아닌, 인물의 내면과 분위기 묘사에 집중할 것.
    3. 결말은 여운이 남도록 구성할 것.
    4. 한국어의 아름다움을 살린 고급 어휘를 선택할 것."
    
    try:
        response = model.generate_content(prompt)
        return jsonify({"story": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Render는 10000번 포트를 사용합니다.
    app.run(host='0.0.0.0', port=10000)
