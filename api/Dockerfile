FROM python:3.11
ADD . /api
WORKDIR /api
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["gunicorn","-w 3","-b","0.0.0.0:8000","ppp_responder:app"]
ENV "OPENSHIFT_BUILD_NAME"="pppm-1" "OPENSHIFT_BUILD_NAMESPACE"="pppm"
LABEL "io.openshift.build.name"="pppm-1" "io.openshift.build.namespace"="pppm"
