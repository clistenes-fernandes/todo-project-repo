FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create and set working directory
RUN mkdir /todo-app
WORKDIR /todo-app

ADD . /todo-app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]