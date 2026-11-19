FROM python:3.12-slim
# Setting a folder inside  the  container as  the work dir:
WORKDIR /app
# Copy the filesin  the local folder to put into the work dir
COPY . /app
# when  the container starts, I want  it  to do this:
ENTRYPOINT ["python3","app.py"]

# docker comands 
# docker volume create calculator_app

# docker build  -t calculator_app_v1  .
# docker run --rm -v calculator_app:/data calculator_app_v1
# docker run --rm -v calculator_app:/data --entrypoint cat calculator_app_v1 /data/my_calc.txt

#Task:
#    Build and run a docker container that uses our calculator and outputs 247/12.

#    S1: Try to persist the answers in a docker volume.
