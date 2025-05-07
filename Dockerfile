# Use the official ContinuumIO Miniconda3 image
FROM continuumio/miniconda3

# Set the working directory in the container
WORKDIR /app

# Copy the environment.yml file into the container
COPY environment.yml .

# Create the conda environment
RUN conda env create -f environment.yml

# Initialize conda in bash
RUN conda init bash

# Add conda environment activation to bash script
SHELL ["/bin/bash", "-c"]

# Make RUN commands use the new environment
RUN echo "conda activate industrialenergy" >> ~/.bashrc

# Copy the entire application code into the container
COPY . .

# Expose the port that the app runs on
EXPOSE 8051

# Set PYTHONPATH environment variable
ENV PYTHONPATH=/app

# Set SHELL to bash with conda environment activated
SHELL ["/bin/bash", "-c"]

# Command to run the application with the conda environment activated
CMD ["conda", "run", "--no-capture-output", "-n", "industrialenergy", "python", "-u", "dashboard_app/server.py"]