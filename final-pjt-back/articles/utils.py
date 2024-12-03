from .models import Article  # Article 모델 임포트
import openai
import json
from .serializers import ArticleListSerializer
from django.conf import settings

def get_finance_answer(prompt):
    # OpenAI API 키 설정
    API_KEY_GPT = settings.API_KEY_GPT

    openai.api_key = API_KEY_GPT

    # type이 'column'인 Article 데이터 가져오기
    related_columns = Article.objects.filter(type='column')[:10]  # 최근 5개 가져오기


    serializer = ArticleListSerializer(related_columns,many=True)  # JSON 형태로 변환
    # ChatGPT API 호출
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "당신은 금융 사이트 폴라리치의 Q&A 섹션 답변을 맡은 금융 전문가입니다. 당신은 사용자가 제시하는 금융 관련 질문에 대해, 사용자가 질문에 사용한 언어로 답변해주어야 합니다. 답변의 첫마디는 '반갑습니다, 폴라리치의 24시간 근무중인 ai 전문가, 메카베어입니다!'가 되어야 합니다. 또한, 사용자의 질문과 관련 있을 수 있는 금융 칼럼도 함께 추천해 주세요. 다만, 답변 형식의 구성은 프론트에서 v-html을 사용함을 고려해주세요. 각 칼럼은 'http://localhost:5173/article/(article의 id)'로 제공됩니다. 다만, 확실히 관련있는 정보를 제공해야 하므로 칼럼 링크의 경우 관련있는 칼럼이 없다 생각한다면 제공하지 않아야 합니다. 칼럼을 제공할 땐 작성자의 닉네임과 제목을 명시하여야 합니다. 마지막으로, 'AI 답변 서비스에 대해선 ai가 실수를 할 수 있으며, 폴라리치 웹 사이트는 해당 답변을 부주의하게 따른 결과에 대하여 책임을 지지 않습니다.' 라는 문구, 유저들이 직접 관련 주제 정보를 찾을 수 있는 한국어 웹사이트 주소 등을 첨부해줘. 답변의 내용은 인사말 이후로 1. 2. 3. 이런 식으로 섹션을 제공해 줘야 하고, 마크다운 형식의 답변을 제공해줘."
            },
            {
                "role": "user",
                "content": f"{prompt}\n\n추천 관련 칼럼 데이터: {serializer.data}"
            }
        ]
    )

    # ChatGPT API 응답 반환
    return response['choices'][0]['message']['content']
