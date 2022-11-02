# Sentence_Extraction

내용 참고 👉🏻 https://www.notion.so/c475ae61d1674b65bde2f4b27e241b9f

## 

1) 특징 잡기 (categories)

2) 어떻게 파싱할지 사례 찾아보기

3) 들어가지 않은 내용 특징 파악하기 → 누락시 어떻게 할 건지 아이디어 

4) 임베딩 방식 정하기 

핵심 문장 추출(extractive approaches) - Text Rank 사용 

Text Rank: 글에서 특정 단어가 다른 문장과 얼마만큼의 관계를 맺고 있는지 계산함 

- Assessment 전까지의 모든 내용

## 질문

## 활용가능한 방향 (아이디어)

1. **문장**으로 요약

요약소견서에 적힌 내용처럼 초진을 요약하는 방안

- Pros: 본 목적
- Cons: 파싱이 잘못되어 중요한 내용이 빠져있으면 2차로 확인을 해야함
    
    실현 가능성이 적음(파싱할 내용이 복잡하고 불규칙적임)
    
1. **카테고리**로 요약하기 (예시: 네이버 쇼핑 리뷰)
- Pros: 내용 파악 쉬움(사용자가 이용할 때 가장 편리한 방안)
- Cons: 실현 가능성 적음 (잘 구현된 모델로 딥러닝)

- 착용감, 만족도, 가격 카테고리를 나눠 문장을 분류함

1. **단어나 짧은 문장 카테고리 별 정리(요약X)**

요약소견서에 중요하다고 적힐 만한 내용을 단어 몇 개나 짧은 문장으로 정리하는 방안

- Pros: 가장 실현가능성 높음
- Cons: 지저분해 보일 수 있음 / 중요 내용이 잘 눈에 안 들어 올 수 있음

+ 모든 초진내용을 볼 수 있게 하되 한눈에 파악이 가능하도록 중요 단어에 하이라이트 표기

**3가지 카테고리: 1. Attack 2. Medical History 3. (Social) Remarks**

**카테고리 별 색을 다르게

의사들이 “편집할 수 있다”는 점을 활용해서 무엇이 중요한지 전문가들이 업데이트 가능하도록 

결국, 처음엔 시스템 내에서 추천하는 중요 문장을 보여주고 의사들이 거기에 빼거나 추가할 수 있게 해놓음 

## 외래 초진 카테고리화

### Gout Attack

#Attack관련정보

- 1st attack 시기 (ex. 1st attack: 7년전)
- attack(통증) 횟수, 증상, 위치, 기간 (ex. 연간 1-2회, 붉었으나 아프지 않았음, Rt 1st MTP, 1주 약 먹고 호전)
- 가장 최근 Attack

### Medical History(Past History, Physical Examination)

#의료히스토리 #신체검사자료 #의뢰내용

- 의뢰 내용
- Past History
    - 복용 중인 약물의 기간, 약명 (ex. 2-3년 전부터, allopurinol)
    - 이전 내원 시기, 원인 (ex. 올해, 통풍발작 2번)
    - 외부 병원 정보, 외부 lab result
- Physical Examination
    - (+/-):
        - 요로결석
        - tophi
        - hypertension
        - Tuberculosis
        - DM
        - RF

### Remarks(Social History, Family History)

#특이사항

- 가족력 (Family History) 유무
    - Gout or Non-gout(etc. 당뇨병)
- Social History
    - 직업
    - social drinking 유무 (음주 유무)
        - ‘+’라면 얼마나 자주
    - 담배 유무
