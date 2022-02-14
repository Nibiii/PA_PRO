#!/bin/bash
docker build -t pa-simulation core/
docker build -t pa-ui ui/
docker build -t pa-backend backend/