# Health authority UI

A user interface for physicians to generate validation codes for their sick
patients, so they can declare themselves as covid+ in their app.

This user interface is tailored to be used in front of a backend architecture
for _decentralized contact tracing_, such as
[dp3t-ms](https://github.com/jdesboeufs/dp3t-ms), and is written in french.

The user interface will require the following API endpoints accessible:

- `/login`
- `/logout`
- `/user-info`: should return a 200 status code if logged in
- `/create-code`: see [dp3t-ms](https://github.com/jdesboeufs/dp3t-ms#codes-microservice)

## Prerequisites

This user interface does not have any dependencies. There is one external
library for generating QR codes that has been copied to this repository:
[qrcodejs](https://github.com/davidshimjs/qrcodejs).

## Configuration

The URLs to the API endpoints are listed at the top of the `index.js` file.

Install keycloak component as Authentication system with protocol open connect:

``` 
docker run -p 7777:8080 --name test-keycloak \
  -e KEYCLOAK_USER=user \
  -e KEYCLOAK_PASSWORD=password \
  -e DB_VENDOR=H2 \
  -d jboss/keycloak
```

Configure a client, and some usesr, then fill the variable environment:

```.env
    AUTHMACHINE_URL=http://192.168.64.3:7777/auth/realms/master
    AUTHMACHINE_CLIENT_ID=myclient
    AUTHMACHINE_CLIENT_SECRET=secret
    AUTHMACHINE_API_TOKEN=
```

Fill the other env variales:
- BACKEND_URL is used by the frontend to defined the backend endpoint
- FRONT_URL is used by the backend for redirection.

```.env
    BACKEND_URL=http://127.0.0.1:8000
    FRONT_URL=http://127.0.0.1:8080
```

## Running a production instance

```
make build
make run
```

## Development

### Front-end

http://localhost:8080

### Backend

http://localhost:8000


## License

MIT