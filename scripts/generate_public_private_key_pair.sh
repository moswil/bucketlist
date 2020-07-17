#!/usr/bin/env bash

source .env

# TODO: check if openssl is installed,
# if not, check the OS, and download and install it

# Generate a 2048 bit RSA Key
# openssl genpkey -aes-256-cbc -pass pass:$KEY_PASSWD -algorithm RSA -out $PRIV_KEY -pkeyopt rsa_keygen_bits:$PRIV_KEYSIZE

# Export the RSA Public Key to a File
# openssl rsa -in $PRIV_KEY -passin pass:$KEY_PASSWD -outform PEM -pubout -out $PUB_KEY

# Permissions for the keys: TODO

# Passphrase-less
# Generate a 2048 bit RSA Key

# FOR ACCESS TOKEN
openssl genpkey -algorithm RSA -out $PRIV_ACCESS_TOKEN_KEY -pkeyopt rsa_keygen_bits:$PRIV_KEYSIZE

# Export the RSA Public Key to a File
openssl rsa -in $PRIV_ACCESS_TOKEN_KEY -outform PEM -pubout -out $PUB_ACCESS_TOKEN_KEY

# FOR REFRESH TOKEN
openssl genpkey -algorithm RSA -out $PRIV_REFRESH_TOKEN_KEY -pkeyopt rsa_keygen_bits:$PRIV_KEYSIZE

# Export the RSA Public Key to a File
openssl rsa -in $PRIV_REFRESH_TOKEN_KEY -outform PEM -pubout -out $PUB_REFRESH_TOKEN_KEY

# Permissions for the keys: TODO
