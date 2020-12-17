# Logstash Configuration Files
This part of the project contains logstash configuration files that will process and parse files CSV files saved by the python script in `/home/elk/Offenses` notice here that I am storing my AQL search results in Offenses folder at `elk` user's home folder.

>PS : Please see the index template definition to have basic understanding of the defined fields used in this project.

Logstash pipelines ar organized in three parts :
- **Input configurations** : Make an input configuration for each file you wanna ingest into elasticsearch.
>Example :
>```
>input {
>    file {
>            path => "/home/<USER>/<FOLDER NAME>/<FILENAME>.csv"
>            start_position => beginning
>            tags => "<MY_CLIENT>"
>            type => "OFFENSES"
>        }
>}
>```
- **Filter configuration** : For processing and enriching the incoming data and normalizing event fields.
- **Output configuration** : Used for sending data to Elasticsearch.
>Example :
>```
>output {
>    if [type] == "OFFENSES" {
>        elasticsearch {
>            hosts => ["https://localhost:9200"]
>            index => "soc-statistics-offenses-%{[client][name]}-%{+yyyy.MM}"
>            #manage_template => false
>            cacert => "/etc/logstash/root-ca.pem"
>            user => "<USERNAME>"
>            password => "<PASSWORD>"
>            ssl => true
>          ssl_certificate_verification => false
>        }
>    }
>}
>```