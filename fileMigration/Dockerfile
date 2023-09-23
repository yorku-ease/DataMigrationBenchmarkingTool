FROM python:3
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

#ENTRYPOINT ["tail"]
#CMD ["-f","/dev/null"]

CMD [ "python", "-u", "./Main.py" ]

#docker run --privileged --memory="0" --cpus="0" -v "$(pwd)"/data:/app/data -v "$(pwd)"/configs:/app/configs -v "$(pwd)"/output:/app/output test