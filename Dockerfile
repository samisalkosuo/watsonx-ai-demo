FROM docker.io/python:3.11-slim

WORKDIR /app

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8echo 
ENV DEBUG_PRINT false

COPY requirements.txt ./
RUN pip install -r requirements.txt && \
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

COPY app ./

#CMD ["bash"]
CMD ["bash", "scripts/start.sh"]
