# Lab03

## Assignment

### 명세

좌우로 움직이면서 blink 하는 삼각형 띄우기

### 해결

매 시간 uniform으로 sin값을 넘겨주고 그 값을 이용해 shader에서 x좌표와 rgb값을 조정함

이때 원래 color에 uniform으로 받은 값을 곱해 원래 색과 검정색을 왔다갔다 하게 하고 position의 x좌표에만 그 값을 더해 좌우로 움직이게 함
