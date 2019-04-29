#pyContextNLP dockerized version

### RUN
    
    $ docker run --rm -p 9999:9999 maastrodocker/pycontextnlp
            
   pyContextNLP optional arguments are
   
   --modifiers=
   
   --targets=
      
   Example of running pyContextNLP using a custom modifier and target file from the host system.
    
    $ docker run --rm\
    -v '/data/KB/critical_findings_lung_embolism_nl.yml:/opt/pyContextNLP/KB/manual_targets.yml'\
    -v '/data/KB/lexical_kb_05042016_nl.yml:/opt/pyContextNLP/KB/custom_modifiers.yml'\
    -e OPTIONAL_ARGS='--targets=/opt/pyContextNLP/KB/manual_targets.yml --modifiers=/opt/pyContextNLP/KB/custom_modifiers.yml'\
    -p 9999:9999 maastrodocker/pycontextnlp

    
   Optional TCP arguments can be found [here](https://github.com/dturanski/springcloudstream)
    
    $ docker run --rm -e OPTIONAL_ARGS='--debug --monitor-port=9999' -p 9999:9999 maastrodocker/pycontextnlp

    
### TCP communication

For communication netcat can be used or see [test_tcp_service](../tests/pyConTextNLP/test_tcp_service.py) for a python implementation

Object parameters:

    text: input text
    targets: optional array of additional pyContextNLP targets (use lowercasing for keys)

Example:

    {"text": "Er zijn weke delen zichtbaar", "targets": [{"direction": "", "lex": "wd", "regex": "weke\\\\s{0,1}delen|wda", "type": "TUMOR"}]}

### NetCat
    
Connect to the application.
    
    nc localhost 9999
    
#### NetCat examples
    
1. The following request (without context):    
    
        {"text": "Er zijn weke delen zichtbaar", "targets": [{"direction": "", "lex": "wd", "regex": "weke\\\\s{0,1}delen|wda", "type": "TUMOR"}]}
    Results in the following response

        [{"found_phrase": "weke delen", "span_start": 8, "span_end": 18, "category": ["tumor"]}]
    
2. The following request (with context):
        
        {"text": "Er zijn geen weke delen zichtbaar", "targets": [{"direction": "", "lex": "wd", "regex": "weke\\\\s{0,1}delen|wda", "type": "TUMOR"}]}
    Results in the following response:
        
        [{"found_phrase": "weke delen", "span_start": 13, "span_end": 23, "category": ["tumor"], "modifier_category": ["definite_negated_existence"], "modifier_found_phrase": "geen"}]


### BUILD (OPTIONAL)

    $ docker build -t maastrodocker/pycontextnlp -f docker/Dockerfile .
    

### Caching

WARNING! Be aware of the following [issue](https://github.com/chapmanbe/pyConTextNLP/issues/13)
After changing a regular expression of a Lex, the application has to be rebooted to clear its cached Regex.