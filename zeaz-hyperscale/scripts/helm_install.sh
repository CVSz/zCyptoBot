#!/usr/bin/env bash
set -e
helm upgrade --install zeaz ./helm/zeaz -n zeaz --create-namespace
