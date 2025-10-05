FROM python:3.11-slim

# Copy all necessary files and directories
COPY ./gui.py /chatIMPACT/gui.py
COPY ./dao.py /chatIMPACT/dao.py
COPY ./utils.py /chatIMPACT/utils.py
COPY ./pages /chatIMPACT/pages
COPY ./static /chatIMPACT/static
COPY ./.streamlit /chatIMPACT/.streamlit
COPY ./local_data /chatIMPACT/local_data
COPY ./requirements.txt /chatIMPACT/requirements.txt

WORKDIR /chatIMPACT

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose port 8501 (Streamlit's default port)
EXPOSE 8501

# Health check to ensure the app is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8501 || exit 1

# Run the Streamlit app
CMD ["streamlit", "run", "gui.py", "--server.port=8501", "--server.address=0.0.0.0"]
