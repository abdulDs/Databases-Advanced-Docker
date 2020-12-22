# getting a python image with a light linux
FROM nickgryg/alpine-pandas

RUN apk add --no-cache gcc musl-dev linux-headers

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ .

CMD ["python", "./scraper.py"]
