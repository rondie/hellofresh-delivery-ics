FROM python:3.11.1 AS builder

ENV LANG=C.UTF-8
ENV PATH="/venv/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

RUN python -m venv /venv

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt


FROM python:3.11.1 AS runner

ENV HOME /app
ENV LANG=C.UTF-8
ENV PATH="/venv/bin:$PATH"

WORKDIR /app

RUN mkdir /output

COPY --from=builder /venv /venv
COPY hellofresh-delivery-ics.py /app/hellofresh-delivery-ics.py

ENTRYPOINT ["python3", "hellofresh-delivery-ics.py"]
