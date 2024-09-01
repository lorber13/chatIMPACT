FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    curl
COPY . /home/ChatIMPACT_GUI/
RUN pip3 install -r /home/ChatIMPACT_GUI/requirements.txt
WORKDIR /home/ChatIMPACT_GUI

COPY . /home/ChatIMPACT_GUI/
EXPOSE 80
HEALTHCHECK CMD curl --fail http://localhost:80/_stcore/health

ENTRYPOINT ["streamlit", "run", "gui.py", "--server.port=80"]
