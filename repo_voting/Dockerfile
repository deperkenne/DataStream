FROM python:3.11

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install coverage


COPY . .

CMD ["sh", "-c", "coverage run -m pytest test.py  && coverage report -m "]
