# This script creates a .env file with the necessary environment variables for the application to run.
# It use the Scaleway CLI to access the secrets stored in the Scaleway Secret Manager.
EMAIL=$(scw secret version access-by-path secret-name=email secret-path=/ revision=1 | grep Data | awk '{print $2}' | base64 -d)
CHAINLIT_AUTH_SECRET=$(scw secret version access-by-path secret-name=chainlit-auth-secret secret-path=/ revision=1 | grep Data | awk '{print $2}' | base64 -d)
OPENAI_API_KEY=$(scw secret version access-by-path secret-name=openai-api-key secret-path=/ revision=1 | grep Data | awk '{print $2}' | base64 -d)

echo "APP_NAME=$APP_NAME" > .env
echo "EMAIL=$EMAIL" >> .env
echo "CHAINLIT_AUTH_SECRET=$CHAINLIT_AUTH_SECRET" >> .env
echo "OPENAI_API_KEY=$OPENAI_API_KEY" >> .env