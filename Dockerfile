FROM docker.io/python:3.10-slim

WORKDIR /app

# streamlit-specific commands for config
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8echo 

# OS Update
RUN apt-get update --allow-unauthenticated -y && \
    pip install -U cffi pip setuptools argon2_cffi chardet watchdog streamlit && \
    pip install --upgrade streamlit-extras && \
    pip install python-dotenv st-clickable-images && \
    pip install --no-cache-dir ibm-watson-machine-learning && \
    mkdir -p /.streamlit && \
    chmod 777 /.streamlit && \
    bash -c 'echo -e "\
[general]\n\
email = \"\"\n\
" > /.streamlit/credentials.toml' && \
    bash -c 'echo -e "\
[server]\n\
enableCORS = false\n\
enableXsrfProtection = false\n\
enableWebsocketCompression = false\n\
" > /.streamlit/config.toml'

EXPOSE 8080

ENV DEBUG_PRINT false

COPY . ./

CMD ["bash", "/app/start.sh"]
