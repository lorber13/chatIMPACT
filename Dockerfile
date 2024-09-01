FROM python:3.11-slim

COPY ./gui.py /chatIMPACT/gui.py
COPY ./dao.py /chatIMPACT/dao.py
COPY ./utils.py /chatIMPACT/utils.py
COPY ./auth.py /chatIMPACT/auth.py
COPY ./pages /chatIMPACT/pages
COPY ./static /chatIMPACT/static
COPY ./.streamlit /chatIMPACT/.streamlit
COPY ./requirements.txt /chatIMPACT/requirements.txt

WORKDIR /chatIMPACT

RUN pip3 install -r /chatIMPACT/requirements.txt

EXPOSE 80

CMD ["streamlit", "run", "gui.py", "--server.port=80"]
