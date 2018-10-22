### BUILD

    $ docker build -t maastrodocker/pycontextnlp -f docker/Dockerfile .

### RUN
    
    $ docker run --rm -p 9999:9999 maastrodocker/pycontextnlp
    
    $ docker run --rm -e PORT=9922 -p 9922:9922 maastrodocker/pycontextnlp 

    
### NetCat
    
    Connect to the application.
    
        nc localhost 9999
    
    The following request:    
    
    $ docker run --rm -p 9999:9999 maastrodocker/pycontextnlp