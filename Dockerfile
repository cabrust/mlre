FROM python:3.7-stretch

# Dependencies
RUN python3.7 -m pip install -U pip setuptools

# Copy app and install in development mode
COPY . /mlre_root
RUN cd /mlre_root && python3.7 setup.py develop

# Run as an ordinary user
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

# This is our app, listen at port 5000
ENV FLASK_APP mlre.radar.radar_app:create_default_app
EXPOSE 5000

# Run it
CMD flask run --host=0.0.0.0
