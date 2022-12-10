FROM ghcr.io/joshkarpel/spiel:v0.4.2

RUN : \
 && apt-get update \
 && apt-get install -y libasound2-dev \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* \
 && :

WORKDIR /app

COPY .. /app/pytest-its-whats-for-testing
RUN pip install --no-cache-dir /app/pytest-its-whats-for-testing

CMD ["spiel", "present", "pytest-its-whats-for-testing/pytest_its_whats_for_testing/slides.py"]
