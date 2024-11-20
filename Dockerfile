FROM python:3.9-slim


# Set the working directory
WORKDIR /app

RUN apt update && apt install -y gcc

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt


COPY app /app

# Make port 80 available to the world outside this container
EXPOSE 80


RUN ./manage.py makemigrations \
&& ./manage.py migrate \
&& ./manage.py collectstatic

CMD ["./manage.py", "runserver", "--insecure", "0.0.0.0:80"]
