# 환경설정
./run.sh 

# cuda env
conda activate thinkgrasp

# ThinkGrasp/assets 에 파일 다운로드
    ├── simplified_objects
    ├── unseen_objects_40
    └── unseen_objects
*** simulation 은 unseen objects 40만 사용함 이때 data를 hugging face (drive 말고) 에서 받아올 것

# Running the simulation (github 따라하기)

# Grounding Dino
pip install git+https://github.com/IDEA-Research/GroundingDINO.git



# Real robot setup

pip install "Flask==2.2.5" "Werkzeug==2.2.3"
