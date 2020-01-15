# maastrodocker/pycontextnlp

Run pyContextNLP as a micro-service and communicate over REST.

Targets can be realtime provided using the JSON-NLP format.

## RUN

    $ docker run \
      --rm \
      -p 5003:5003 \
      -e 'TARGETS=https://raw.githubusercontent.com/putssander/medstruct-config/master/pycontextnlp/pycontextnlp_tnm_targets_nl.yml' \
      -e 'MODIFIERS=https://raw.githubusercontent.com/putssander/medstruct-config/master/pycontextnlp/pycontextnlp_modifiers_nl.yml' \
      maastrodocker/pycontextnlp


#### GET 
[http://localhost:5003?text=Er is geen tumor aanwezig](http://localhost:5003?text=Er is geen tumor aanwezig)

#### POST 
    
    curl -d '{"text": "Er zijn weke delen zichtbaar", "targets": [{"direction": "", "lex": "weke", "regex": "weke", "type": "TUMOR"}]}'  -H "Content-Type: application/json" -X POST http://localhost:5003/

#### POST (JSON-NLP) 

Use the JSON-NLP endpoint [/json-nlp](/json-nlp) and post a document in json-nlp format,
Entities present in the json-nlp document, which a certain entity category (set with environment variable ENTITY_TYPES), will be added to the targets to validate.

An layer "context" will be added to the JSON-NLP document, containing the context results.

See an example of an pipeline including configuration [here](https://github.com/putssander/medstruct-config).


### Configuration

Regex has to be defined using single quotes '' (no double quotes "")
For running on local pyContextNLP target and modifier files [this](https://github.com/putssander/medstruct-config) docker-compose configuration.

      Lex: mogelijk
      Type: PROBABLE_EXISTENCE
      Regex: 'mogelijk'
      Direction: bidirectional
      Unnamed-4: 2/28/2013
      Unnamed-5: ""
      Unnamed-6: ""
      Codes: ""
    ---
    


### Manual docker build

    $ docker build -t maastrodocker/pycontextnlp .
    
### ISSUES

#### Caching Problem
WARNING! Be aware of the following [issue](https://github.com/chapmanbe/pyConTextNLP/issues/13).
After changing a regular expression of a "Lex", the application has to be rebooted to clear its cached "Rex".