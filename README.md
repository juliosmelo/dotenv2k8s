## Why this?
I'm assuming that you're using the declarative Kubernetes format for setup your workload.

Well... I was working on a project with more than 40 .env (dotenv) files in multiple projects that implements the [12factor](https://12factor.net/) methodology. However they were using clear text env vars with sensitive keys, tokens and data on the PODs spec to make the workloads run into a Kubernetes cluster. 

As we know (this is not safe.)[https://kubernetes.io/docs/concepts/configuration/secret/#information-security-for-secrets]

So I decided to move all of that clear text env vars to Kubernetes [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/#creating-a-secret). But wait... more than 40 .env (dotenv), such a bored task to do manually :neutral_face: . I hope this helps you as has helped me. 


## How it works

Let's say that you have an .env (dotenv) file with this content that you want to create a Kubernetes Secret object.

```bash
USERNAME=username
PASSWORD=password
```
All you need to do is
```bash
pip install dotenv2k8s
dotenv2k8s --path=/path/to/the/dotenv/.env

Secret name: my-secret
Kubernetes Namespace [default]: my-namespace
```
```bash
You can also to do this to achieve the same result

dotenv2k8s --path=/path/to/the/dotenv/.env --name=my-secret --namespace=my-namespace
```
Where:

- path: is the absolute path to the .env (dotenv) file

- Secret name: is the name of the object

- Kubernetes Namespace [default]: is the namespace of where the secret will be available ( default is the k8s 'default' namespace)

You will ended up with a file named `secret-my-secret-my-namespace.yaml` with the content

Another suggestion is to put this tool in a shell script that does it at once, for instance:

```

```

```yaml
YAML output

apiVersion: v1
data:
  USERNAME: YWRtaW4=
  PASSWORD: MWYyZDFlMmU2N2Rm
kind: Secret
metadata:
  name: my-secret
  namespace: my-namespace
type: Opaque
---
# POD spec for more information go to https://kubernetes.io/docs/concepts/configuration/secret/#using-secrets-as-environment-variables
- name: USERNAME
  valueFrom:
    secretKeyRef:
      key: USERNAME
      name: my-secret
      optional: false
- name: PASSWORD
  valueFrom:
    secretKeyRef:
      key: PASSWORD
      name: my-secret
      optional: false

```

To conclude, create the object in the cluster, use it on the PODs and paste the POD spec into the POD manifest.

```bash
kubectl apply -f secret-my-secret-my-namespace.yaml
```