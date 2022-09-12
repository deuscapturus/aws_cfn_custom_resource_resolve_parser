#!/usr/bin/env python

"""Tests for `aws_cfn_custom_resource_resolve_parser` package."""

import pytest
import boto3
from os import path


from aws_cfn_custom_resource_resolve_parser import parse_secret_resolve_string


def test_parsing_arn():
    secret = (
        r"{{resolve:secretsmanager:arn:aws:secretsmanager:eu-west-1:012345678912:secret:/kafka/eu-west-1/server01"
        r":SecretString:BOOTSTRAP_SERVERS}}"
    )
    secret_value = parse_secret_resolve_string(secret)
    assert (
        secret_value[0]
        == "arn:aws:secretsmanager:eu-west-1:012345678912:secret:/kafka/eu-west-1/server01"
    )
    assert secret_value[1] == "BOOTSTRAP_SERVERS"

def test_parsing_arn_with_key_missing_versions():
    secret = (
        r"{{resolve:secretsmanager:arn:aws:secretsmanager:eu-west-1:012345678912:secret:kafka/eu-west-1/server01"
        r":SecretString:BOOTSTRAP_SERVERS::}}"
    )
    secret_value = parse_secret_resolve_string(secret)
    assert (
        secret_value[0]
        == "arn:aws:secretsmanager:eu-west-1:012345678912:secret:kafka/eu-west-1/server01"
    )
    assert secret_value[1] == "BOOTSTRAP_SERVERS"

def test_parsing_arn_with_only_version_id():
    secret = (
        r"{{resolve:secretsmanager:arn:aws:secretsmanager:eu-west-1:012345678912:secret:kafka/eu-west-1/server01"
        r":SecretString:::7b4bdaaa-32b5-11ed-8bdc-00051bcc25e0}}"
    )
    secret_value = parse_secret_resolve_string(secret)
    assert (
        secret_value[0]
        == "arn:aws:secretsmanager:eu-west-1:012345678912:secret:kafka/eu-west-1/server01"
    )
    assert secret_value[3] == "7b4bdaaa-32b5-11ed-8bdc-00051bcc25e0"

def test_parsing_arn_with_missing_version_and_key():
    secret = (
        r"{{resolve:secretsmanager:arn:aws:secretsmanager:eu-west-1:012345678912:secret:kafka/eu-west-1/server01"
        r":SecretString:::}}"
    )
    secret_value = parse_secret_resolve_string(secret)
    assert (
        secret_value[0]
        == "arn:aws:secretsmanager:eu-west-1:012345678912:secret:kafka/eu-west-1/server01"
    )

def test_parsing_arn_with_key_and_version_stage():
    secret = (
        r"{{resolve:secretsmanager:arn:aws:secretsmanager:eu-west-1:012345678912:secret:kafka/eu-west-1/server01"
        r":SecretString:BOOTSTRAP_SERVERS:AWSCURRENT:}}"
    )
    secret_value = parse_secret_resolve_string(secret)
    assert (
        secret_value[0]
        == "arn:aws:secretsmanager:eu-west-1:012345678912:secret:kafka/eu-west-1/server01"
    )
    assert secret_value[1] == "BOOTSTRAP_SERVERS"
    assert secret_value[2] == "AWSCURRENT"

def test_parsing_name():
    secret = r"{{resolve:secretsmanager:/kafka/eu-west-1/server01:SecretString:BOOTSTRAP_SERVERS::AWSPENDING}}"
    secret_value = parse_secret_resolve_string(secret)
    assert secret_value[0] == "/kafka/eu-west-1/server01"
    assert secret_value[1] == "BOOTSTRAP_SERVERS"
    assert secret_value[2] == "AWSPENDING"