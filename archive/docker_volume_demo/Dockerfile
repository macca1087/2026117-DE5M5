FROM python:3.12-slim
# Setting a folder inside  the  container as  the work dir:
WORKDIR /app
# Copy the filesin  the local folder to put into the work dir
COPY . /app
# when  the container starts, I want  it  to do this:
ENTRYPOINT ["python3","app.py"]

# docker comands 
# docker volume create hello-vol

# docker build  -t hello-vol-v1
# docker run --rm -v hello-vol:/data hello-vol-v1


#Task:
#    Build and run a docker container that uses our calculator and outputs 247/12.

#    S1: Try to persist the answers in a docker volume.
