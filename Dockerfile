FROM python:3.11.2 AS builder

ENV LANG=C.UTF-8
ENV PATH="/venv/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

RUN python -m venv /venv

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt


FROM python:3.11.2 AS runner

ENV HOME ${APPDIR}
ENV LANG=C.UTF-8
ENV PATH="/venv/bin:$PATH"
ENV HELLOFRESH_ICS_UID=1000
ENV HELLOFRESH_ICS_GID=1000
ARG APPDIR="/app"

RUN addgroup --gid ${HELLOFRESH_ICS_UID} --system app && \
    adduser --no-create-home --shell /bin/false --disabled-password --uid ${HELLOFRESH_ICS_GID} --system --group app
RUN mkdir ${APPDIR} && \
    chown -R ${HELLOFRESH_ICS_UID}:${HELLOFRESH_ICS_GID} ${APPDIR}

USER app

WORKDIR ${APPDIR}

COPY --from=builder /venv /venv
COPY --chown=${HELLOFRESH_ICS_UID}:${HELLOFRESH_ICS_GID} templates/ config.py functions.py app.py ${APPDIR}/

ENTRYPOINT ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
