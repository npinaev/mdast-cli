FROM python:3.9-slim

WORKDIR /mdast_cli

COPY ./ /mdast_cli

RUN pip install -r requirements.txt

RUN pip install poly_app_downloader -U

ENTRYPOINT ["poly_app_downloader"]