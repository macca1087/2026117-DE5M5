FROM python:3.12-slim
# Setting a folder inside  the  container as  the work dir:
WORKDIR /app
# Copy the filesin  the local folder to put into the work dir
COPY . /app
# when  the container starts, I want  it  to do this:
ENTRYPOINT ["python3","hello.py"]

# docker comands 
# docker build  -t myfirstdocker .
# docker run myfirstdocker
