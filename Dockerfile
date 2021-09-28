FROM continuumio/miniconda3:latest
LABEL maintainer "Asher Pembroke <apembroke@gmail.com>"

RUN conda install -y python=3.7
RUN conda install jupyter
RUN conda install jupytext -c conda-forge
RUN conda install -c conda-forge dash pandas scipy numpy networkx
RUN pip install jupyter-dash
RUN pip install dash-bootstrap-components
RUN pip install git+https://github.com/predsci/psidash.git

COPY . /dashboard

RUN pip install -e dashboard

WORKDIR /dashboard

# set up jupyter
RUN jupyter notebook --generate-config
ENV JUPYTER_PASSWORD ''
ENV JUPYTER_PORT 8888
ENV JUPYTER_NOTEBOOKS /dashboard

CMD ["sh", "-c", "chmod +x /dashboard/jupyter_run.sh && /dashboard/jupyter_run.sh"]
