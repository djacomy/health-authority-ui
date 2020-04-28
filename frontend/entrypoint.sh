#!/bin/bash

cd /srv/staticapp
npm install
envsubst < public/static/env-templ.js > public/static/env.js

exec "$@"