# Use a base image with RDP server and necessary tools
FROM ubuntu:20.04

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Install required packages
RUN apt-get update && apt-get install -y \
    xfce4 \
    xfce4-goodies \
    xrdp \
    ffmpeg \
    x11vnc \
    xvfb \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up RDP
RUN sed -i 's/port=3389/port=3390/' /etc/xrdp/xrdp.ini

# Create a script to start services and capture screen
RUN echo '#!/bin/bash\n\
Xvfb :1 -screen 0 1920x1080x24 &\n\
export DISPLAY=:1\n\
startxfce4 &\n\
x11vnc -display :1 -nopw -forever &\n\
ffmpeg -f x11grab -framerate 30 -video_size 1920x1080 -i :1 -c:v libx264 -preset ultrafast -crf 23 /output/screen_recording.mp4\n\
' > /start_and_record.sh \
&& chmod +x /start_and_record.sh

# Create a directory for the output
RUN mkdir /output

# Expose RDP port
EXPOSE 3390

# Start the services and begin recording
CMD ["/start_and_record.sh"]