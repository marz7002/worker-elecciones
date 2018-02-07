# worker-elecciones

This script downloads and transform tweets of potential presidential candidates for 2018.

`docker build -t worker .`

``
docker run -t -d -P\
 -e API_KEY="<>" \
 -e API_SECRET="<>" \
 -e ACCESS_TOKEN_KEY="<>" \
 -e ACCESS_TOKEN_SECRET="<>" \
 -e AWS_ACCESS_KEY_ID="<>" \
 -e AWS_SECRET_ACCESS_KEY="<>" \
 --name worker-elecciones \
 worker
``
