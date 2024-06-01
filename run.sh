#! /bin/zsh
lsof -t -i tcp:8000 | xargs kill -9
#8000번 포트에서 돌아가는 프로세스 찾아서 종료
python3 manage.py runserver 0.0.0.0:8000