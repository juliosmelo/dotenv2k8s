from base64 import b64encode

from dotenv import dotenv_values
from yaml import dump, load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def create_b64encoded_values(data):
    for key, value in data.items():
        encoded_byte_string = b64encode(value.encode("ascii"))
        data[key] = encoded_byte_string.decode("ascii")
    return data


def create_k8s_manifest(dotenv_file, manifest_metadata):
    dotenv = dotenv_values(dotenv_file)
    b64_encoded_data = create_b64encoded_values(dict(dotenv))
    secret_manifest = {
        "apiVersion": "v1",
        "data": b64_encoded_data,
        "kind": "Secret",
        "metadata": manifest_metadata,
        "type": "Opaque",
    }
    manifest = dump(secret_manifest)
    file_name = (
        f"secret-{manifest_metadata['name']}-{manifest_metadata['namespace']}.yaml"
    )
    with open(file_name, "w") as yaml_stream:
        yaml_stream.write(manifest)
    return manifest


def create_pod_spec_as_envvar(data, metadata):
    manifest_data = load(data, Loader)
    spec_list = []
    for key, value in manifest_data["data"].items():
        spec_key = {}
        spec_key["name"] = key
        spec_key["valueFrom"] = {}
        spec_key["valueFrom"]["secretKeyRef"] = {}
        spec_key["valueFrom"]["secretKeyRef"]["name"] = metadata["name"]
        spec_key["valueFrom"]["secretKeyRef"]["key"] = key
        spec_key["valueFrom"]["secretKeyRef"]["optional"] = False
        spec_list.append(spec_key)
    spec_manifest = dump(spec_list)
    return spec_manifest
