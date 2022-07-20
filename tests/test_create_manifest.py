import os
from base64 import b64encode

from yaml import load

from dotenv2k8s.main import create_k8s_manifest, create_pod_spec_as_envvar

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


PATH = os.path.dirname(__file__)
MOCKED_KEY_TO_ENCODE = "AWS_S3_ACCESS_KEY_ID"


def test_create_manifest():
    metadata = {"name": "sweet_secret_secret", "namespace": "sweet_secret"}
    manifest = create_k8s_manifest(os.path.join(PATH, ".env"), metadata)
    manifest_data = load(manifest, Loader)
    assert manifest_data["apiVersion"] == "v1"
    assert manifest_data["type"] == "Opaque"
    assert manifest_data["kind"] == "Secret"
    assert len(manifest_data["data"]) == 8


def test_b64encoded_values():
    metadata = {"name": "sweet_secret_secret", "namespace": "sweet_secret"}
    manifest = create_k8s_manifest(os.path.join(PATH, ".env"), metadata)
    manifest_data = load(manifest, Loader)
    b64_value = b64encode(MOCKED_KEY_TO_ENCODE.encode("ascii"))
    assert manifest_data["data"][MOCKED_KEY_TO_ENCODE] == b64_value.decode("ascii")


def test_create_pod_spec_as_envvar():
    metadata = {"name": "sweet_secret_secret", "namespace": "sweet_secret"}
    manifest = create_k8s_manifest(os.path.join(PATH, ".env"), metadata)
    spec = create_pod_spec_as_envvar(manifest, metadata)
    spec_manifest_data = load(spec, Loader)
    assert len(spec_manifest_data) == 8
