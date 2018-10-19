BUILD

    $ docker build -t maastrodocker/pycontextnlp -f docker/Dockerfile .

RUN
    
    $ docker run --rm -p 9999:9999 maastrodocker/pycontextnlp