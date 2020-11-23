# social_value_analysis

한국어 기반 인터넷 언론사들의 사회적 가치를 토픽 모델링을 통해 분석.

각 언론사의 특징을 분석합니다.

## Examples

<img src="https://user-images.githubusercontent.com/58092114/96550735-2fe43980-12ec-11eb-98e1-e2971eddc239.png" width="400">

한겨레 뉴스 '기업 사회적 가치' 로 검색한 단어들의 워드클라우드. 

<img src="https://user-images.githubusercontent.com/58092114/99935080-2e9ea480-2da3-11eb-8161-25a23c33efea.png" width="600">

전체 크롤링 데이터 t-SNE 시각화.

<img src="https://user-images.githubusercontent.com/58092114/99935145-5aba2580-2da3-11eb-86a3-6c107c73def2.png" width="600">

경향신문 networkx graph 시각화

## References

본 프로젝트의 코드들은 다음 출처의 도움으로 작성되었습니다.

### Overall 
한국어 임베딩 by ratsgo (https://github.com/ratsgo/embedding)
LOVIT X DATA SCIENCE by lovid (https://lovit.github.io/)

#### crawling/crawling.py
크롤링 (5), beautifulsoup4로 네이버 기사 크롤링하기 by 차준영 (https://dsbook.tistory.com/54)
파이썬으로 특정 키워드를 포함하는 신문기사 웹크롤링 & 워드클라우드 시각화 분석 - 3 (동아일보, 한겨레 '사드'관련 기사 크롤링하기) by 윤빵꾸 (https://yoonpunk.tistory.com/6)
파이썬 - OOP Part 5. 상속과 서브 클래스(Inheritance and Subclass) by 이상희 (http://schoolofweb.net/blog/posts/%ED%8C%8C%EC%9D%B4%EC%8D%AC-oop-part-5-%EC%83%81%EC%86%8D%EA%B3%BC-%EC%84%9C%EB%B8%8C-%ED%81%B4%EB%9E%98%EC%8A%A4inheritance-and-subclass/)

#### embedding/word_embedding.py
임베딩 - Word2Vec by Joyhong (https://joyhong.tistory.com/132)

#### visualizing/networkx.py
NetworkX 파이썬 패키지를 이용한 네트워크 그래프 작성 by 유병혁 (http://blog.daum.net/geoscience/1408)

