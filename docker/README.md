### BUILD

    $ docker build -t maastrodocker/pycontextnlp -f docker/Dockerfile .

### RUN
    
    $ docker run --rm -p 9999:9999 maastrodocker/pycontextnlp
            
   pyContextNLP optional arguments are
   
   --modifiers=
   
   --targets=
    
   which have default values.
   
    $ docker run --rm -e OPTIONAL_ARGS='--modifiers=/opt/pyContextNLP/KB/lexical_kb_05042016_nl.yml' -p 9922:9999 maastrodocker/pycontextnlp

   
   Container paths can be overwritten using a volume mount by files form your host.
    
    $ docker run --rm -v '/data/KB/modifiers.yml:/opt/pyContextNLP/KB/modifiers.yml' -e OPTIONAL_ARGS='--modifiers=/opt/pyContextNLP/KB/modifiers.yml' -p 9922:9999 maastrodocker/pycontextnlp

    
   Optional TCP arguments can be found [here](https://github.com/dturanski/springcloudstream)
    
    $ docker run --rm -e OPTIONAL_ARGS='--debug --monitor-port=9999' -p 9922:9999 maastrodocker/pycontextnlp

    
### NetCat
    
    Connect to the application.
    
        nc localhost 9999
    
    The following request:    
    
