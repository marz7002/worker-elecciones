# worker-elecciones

`docker build -t worker .`

``
docker run -t -d -P\
 -e API_KEY="<>" \
 -e API_SECRET="<>" \
 -e ACCESS_TOKEN_KEY="<>" \
 -e ACCESS_TOKEN_SECRET="<>" \
 -e AWS_ACCESS_KEY_ID="AKIAITSLOEFRVYGULPKQ" \
 -e AWS_SECRET_ACCESS_KEY="<>" \
 --name worker-elecciones \
 worker
``