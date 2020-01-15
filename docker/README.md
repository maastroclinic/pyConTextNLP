# maastrodocker/pycontextnlp

Run pyContextNLP as a micro-service and communicate over TCP.

Targets can be provided in the TCP request, this enables the extraction of context for targets are extracted by a another approach (e.g. concept extractor QuickUMLS).


## RUN

    $ docker run \
      --rm \
      -p 5003:5003 \
      -e 'TARGETS=https://raw.githubusercontent.com/putssander/medstruct-config/master/pycontextnlp/pycontextnlp_tnm_targets_nl.yml' \
      -e 'MODIFIERS=https://raw.githubusercontent.com/putssander/medstruct-config/master/pycontextnlp/pycontextnlp_modifiers_nl.yml' \
      maastrodocker/pycontextnlp


GET [http://localhost:5003?text=Er is geen tumor aanwezig](http://localhost:5003?text=Er is geen tumor aanwezig)


### Manual docker build

    $ docker build -t maastrodocker/pycontextnlp .
    
### ISSUES

#### Caching Problem
WARNING! Be aware of the following [issue](https://github.com/chapmanbe/pyConTextNLP/issues/13).
After changing a regular expression of a "Lex", the application has to be rebooted to clear its cached "Rex".