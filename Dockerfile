FROM node:latest as builder


WORKDIR /usr/src/app

COPY js ./js
RUN ls

RUN cd js && npm install


FROM python:3.8

WORKDIR /usr/src/app

COPY . .
RUN pip install --no-cache-dir modin==0.9.1 -r requirements.txt
RUN pip install ray==1.1.0
RUN pip install notebook --upgrade

RUN pip install -e .

COPY --from=builder /usr/src/app/js/dist ./js
RUN jupyter nbextension install --py --symlink --sys-prefix modin_spreadsheet && jupyter nbextension enable --py --sys-prefix modin_spreadsheet

CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]