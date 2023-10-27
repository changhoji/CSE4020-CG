[Home](../README.md)

# Project3 - Bvh Viewer

2021035487 이창호

## Requirements I Implemented

1. load bvh file and render
    1. drae-and-drop으로 bvh파일을 drop하면 파일을 읽고 파싱해 vao들을 만들고, line mode의 rest pose를 rendering함
    2. 1을 누르면 line rendering mode로, 2를 누르면 box rendering mode로 전환됨
        1. box rendering에서 phong illumination과 phong shading을 적용시킴
        2. light position은 view position과 같게 함
    3. 어느 장면 (애니메이션 진행중 이라도) 에서나 모드를 전환하면 즉시 전환됨
2. render skeleton of the motion
    1. offset과 HIERARCY를 이용해 rest pose를 rendering함
    2. 모든 joint들은 연결되어 있음
3. animate the model when press spacebar key
    1. 스페이스바를 누르면 bvh 파일을 읽을 때 저장했던 프레임 정보들을 이용해 joint transform을 변화시키고, 바꾼 joint transform으로 global transform을 update시켜 motion을 적용시킴
    2. frame time을 이용해 frame time만큼의 시간이 지날 때마다 다음 frame을 적용시킴
4. print information of bvh file
    1. drop-and-drop하면 file name, number of frames, fps, number of joints, list of all joint names를 출력함
    2. 이때 end site도 하나의 joint로 취급했음

## Hyperlink To The Video

[animating hierarchical model with bvh format file](https://youtube.com/shorts/IUkncRI5dYk?feature=share)