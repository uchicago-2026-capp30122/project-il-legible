# project-il-legible

## Environment Variables

This project makes use of several APIs that require API keys for endpoint requests. Following these steps, you may set up your own environment file with custom variables defined:

1. Run `touch .env` in the same directory as your `uv.lock` 
2. Run `echo UV_ENV_FILE=.env` to tell where UV where to look for the environment file.
3. Populate the .env file with key-value pairs delimited with an equal sign, e.g. `MY_KEY="123"`

Please ensure that the `.env` file is included in the `.gitignore` and that it IS NOT checked into version control.
