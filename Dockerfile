FROM jupyter/pyspark-notebook:python-3.10

# Set working directory for notebooks
WORKDIR /notebooks

# Fix Sentinel import error
RUN pip install --upgrade typing_extensions

# Install your Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy notebooks and data folders into the container
COPY notebooks/ /notebooks/
COPY data/ /data/

# Start Jupyter Notebook
CMD ["start-notebook.sh"]


