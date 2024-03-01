#
FROM python:3.11.4

#
WORKDIR /code

#
COPY ./requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY src/app /code/app

#
CMD ["uvicorn", "src.app.main:api","--reload", "--host", "0.0.0.0", "--port", "80"]