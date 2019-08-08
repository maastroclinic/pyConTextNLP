# maastrodocker/pycontextnlp

Run pyContextNLP as a micro-service and communicate over TCP.

Targets can be provided in the TCP request, this enables the extraction of context for targets are extracted by a another approach (e.g. concept extractor QuickUMLS).


## RUN
    
    $ docker run --rm -p 9999:9999 maastrodocker/pycontextnlp
            
Provide an optional .yml-file for pyContextNLP targets and modifiers using the following arguments:
   
   --modifiers=...
   
   --targets=...


Example of running pyContextNLP using a custom modifier and target file from the host system.
    
    $ docker run --rm\
    -v '/data/KB/critical_findings_lung_embolism_nl.yml:/opt/pyContextNLP/KB/manual_targets.yml'\
    -v '/data/KB/lexical_kb_05042016_nl.yml:/opt/pyContextNLP/KB/custom_modifiers.yml'\
    -e OPTIONAL_ARGS='--targets=/opt/pyContextNLP/KB/custom_targets.yml --modifiers=/opt/pyContextNLP/KB/custom_modifiers.yml'\
    -p 9999:9999 maastrodocker/pycontextnlp

Replace '/data/KB/critical_findings_lung_embolism_nl.yml' and or '/data/KB/lexical_kb_05042016_nl.yml' with the paths of the host system.
    
Optional TCP arguments can be found [here](https://github.com/dturanski/springcloudstream)
    
    $ docker run --rm -e OPTIONAL_ARGS='--debug --monitor-port=9999' -p 9999:9999 maastrodocker/pycontextnlp
    

REST

    docker run --rm    -v '/data/KB/critical_findings_lung_embolism_nl.yml:/opt/pyContextNLP/KB/manual_targets.yml'    -v '/data/KB/lexical_kb_05042016_nl.yml:/opt/pyContextNLP/KB/custom_modifiers.yml'    -e OPTIONAL_ARGS='--targets=/opt/pyContextNLP/KB/custom_targets.yml --modifiers=/opt/pyContextNLP/KB/custom_modifiers.yml'    -p 8080:80 maastrodocker/pycontextnlp
    
POST

    curl -d '{"text": "Er zijn weke delen zichtbaar", "targets": [{"direction": "", "lex": "weke", "regex": "weke", "type": "TUMOR"}]}'  -H "Content-Type: application/json" -X POST http://localhost:8080/


    
## TCP communication

For communication netcat can be used or see [test_tcp_service](../tests/pyConTextNLP/test_tcp_service.py) for a python implementation or [medstruct](https://github.com/maastroclinic/medstruct)

JSON parameters:
- text: input text  
- targets: optional array of additional pyContextNLP targets (use lowercasing for keys)


#### NetCat example
    
1. Connect to the application.
    
        nc localhost 9999
     
2. The following request:    
    
        {"text": "Er zijn weke delen zichtbaar", "targets": [{"direction": "", "lex": "wd", "regex": "weke\\\\s{0,1}delen|wda", "type": "TUMOR"}]}
    Results in the following response (target without modifier extracted)

        [{"found_phrase": "weke delen", "span_start": 8, "span_end": 18, "category": ["tumor"]}]
    
3. The following request (with context):
        
        {"text": "Er zijn geen weke delen zichtbaar", "targets": [{"direction": "", "lex": "wd", "regex": "weke\\\\s{0,1}delen|wda", "type": "TUMOR"}]}
    Results in the following response (target with modifier extracted)
        
        [{"found_phrase": "weke delen", "span_start": 13, "span_end": 23, "category": ["tumor"], "modifier_category": ["definite_negated_existence"], "modifier_found_phrase": "geen"}]


### Manual docker build

    $ docker build -t maastrodocker/pycontextnlp .


    $ docker build -t maastrodocker/pycontextnlp:tcp -f docker/tcp/Dockerfile .
    

### ISSUES


#### Caching
WARNING! Be aware of the following [issue](https://github.com/chapmanbe/pyConTextNLP/issues/13).
After changing a regular expression of a "Lex", the application has to be rebooted to clear its cached "Rex".