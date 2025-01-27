---
description: Deploying ZenML on cloud using the ZenML CLI.
---

# Deploy with ZenML CLI

The easiest and fastest way to get running on the cloud is by using the `deploy` CLI command. It currently only supports deploying to Kubernetes on managed cloud services. You can check the [overview page](zenml-self-hosted.md) to learn about other options that you have.

Before we begin, it will help to understand the [architecture](zenml-self-hosted.md) around the ZenML server and the database that it uses. Now, depending on your setup, you may find one of the following scenarios relevant.

## Option 1: Starting from scratch

If you don't have an existing Kubernetes cluster, you have the following two options to set it up:

* Creating it manually using the documentation for your cloud provider. For convenience, here are links for [AWS](https://docs.aws.amazon.com/eks/latest/userguide/create-cluster.html), [Azure](https://learn.microsoft.com/en-us/azure/aks/learn/quick-kubernetes-deploy-portal?tabs=azure-cli), and [GCP](https://cloud.google.com/kubernetes-engine/docs/how-to/creating-a-zonal-cluster#before\_you\_begin).
* Using a [stack recipe](../../stacks-and-components/stack-deployment/deploy-a-stack-using-stack-recipes.md) that sets up a cluster along with other tools that you might need in your cloud stack like artifact stores and secret managers. Take a look at all [available stack recipes](https://github.com/zenml-io/mlops-stacks#-list-of-recipes) to see if there's something that works for you.

{% hint style="warning" %}
Once you have created your cluster, make sure that you configure your [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl) client to talk to it.
{% endhint %}

You're now ready to deploy ZenML! Run the following command:

```bash
zenml deploy
```

You will be prompted to provide a name for your deployment and details like what cloud provider you want to deploy to, in addition to the username, password, and email you want to set for the default user — and that's it! It creates the database and any VPCs, permissions, and more that are needed.

{% hint style="info" %}
In order to be able to run the `deploy` command, you should have your cloud provider's CLI configured locally with permissions to create resources like MySQL databases and networks.
{% endhint %}

Reasonable defaults are in place for you already and if you wish to configure more settings, take a look at the next scenario that uses a config file.

## Option 2: Using existing cloud resources

### Existing Kubernetes cluster

If you already have an existing cluster without an ingress controller, you can jump straight to the `deploy` command above to get going with the defaults. Please make sure that you have your local `kubectl` configured to talk to your cluster.

#### Having an existing NGINX Ingress Controller

The `deploy` command, by default, tries to create an NGINX ingress controller on your cluster. If you already have an existing controller, you can tell ZenML to not re-deploy it through the use of a config file. This file can be found in the [Configuration File Templates](deploy-with-zenml-cli.md#configuration-file-templates) towards the end of this guide. It offers a host of configuration options that you can leverage for advanced use cases.

*   Check if an ingress controller is running on your cluster by running the following command. You should see an entry in the output with the hostname populated.

    ```bash
    # change the namespace to any other where 
    # You might have the controller installed
    kubectl get svc -n ingress-nginx
    ```
* Set `create_ingress_controller` to `false`.
*   Supply your controller's hostname to the `ingress_controller_hostname` variable.

    > **Note:** The address should not have a trailing `/`.
*   You can now run the `deploy` command and pass the config file above, to it.

    ```
    zenml deploy --config=/PATH/TO/FILE
    ```

    > **Note:** To be able to run the deploy command, you should have your cloud provider's CLI configured locally with permissions to create resources like MySQL databases and networks.

### Existing hosted SQL database

If you also already have a database that you would want to use with the deployment, you can choose to configure it with the use of the config file. Here, we will demonstrate setting the database.

*   Fill the fields below from the config file with values from your database.

    ```yaml
    # The username and password for the database.
    database_username: 
    database_password: 

    # The URL of the database to use for the ZenML server.
    database_url: 

    # The path to the SSL CA certificate to use for the database connection.
    database_ssl_ca: 

    # The path to the client SSL certificate to use for the database connection.
    database_ssl_cert: 

    # The path to the client SSL key to use for the database connection.
    database_ssl_key: 

    # Whether to verify the database server SSL certificate.
    database_ssl_verify_server_cert: 
    ```
*   Run the `deploy` command and pass the config file above to it.

    ```
    zenml deploy --config=/PATH/TO/FILE
    ```

    > **Note** To be able to run the deploy command, you should have your cloud provider's CLI configured locally with permissions to create resources like MySQL databases and networks.

## Configuration file templates

#### Base configuration file

Below is the general structure of a config file. Use this as a base and then add any cloud-specific parameters from the sections below.

<details>

<summary>General</summary>

```yaml
# Name of the server deployment.
name:

# The server provider type, one of aws, gcp or azure.
provider:

# The username for the default ZenML server account.
username:
password:

# The path to the kubectl config file to use for deployment.
kubectl_config_path:

# The Kubernetes namespace to deploy the ZenML server to.
namespace: zenmlserver

# The path to the ZenML server helm chart to use for deployment.
helm_chart:

# The repository and tag to use for the ZenML server Docker image.
zenmlserver_image_repo: zenmldocker/zenml
zenmlserver_image_tag: latest

# Whether to deploy an nginx ingress controller as part of the deployment.
create_ingress_controller: true

# Whether to use TLS for the ingress.
ingress_tls: true

# Whether to generate self-signed TLS certificates for the ingress.
ingress_tls_generate_certs: true

# The name of the Kubernetes secret to use for the ingress.
ingress_tls_secret_name: zenml-tls-certs

# The ingress controller's IP address. The ZenML server will be exposed on a subdomain of this IP. For AWS, if you have a hostname instead, use the following command to get the IP address: `dig +short <hostname>`.
ingress_controller_ip:

# Whether to create a SQL database service as part of the recipe.
deploy_db: true

# The username and password for the database. 
database_username: user
database_password:

# The URL of the database to use for the ZenML server.
database_url:

# The path to the SSL CA certificate to use for the database connection.
database_ssl_ca:

# The path to the client SSL certificate to use for the database connection.
database_ssl_cert:

# The path to the client SSL key to use for the database connection.
database_ssl_key:

# Whether to verify the database server SSL certificate.
database_ssl_verify_server_cert: true

# The log level to set the terraform client. Choose one of TRACE, 
# DEBUG, INFO, WARN, or ERROR (case insensitive).
log_level: ERROR 
```

</details>

{% hint style="info" %}
Feel free to include only those variables that you want to customize, in your file. For all other variables, the default values (shown above) will be used.
{% endhint %}

#### Cloud-specific settings

{% tabs %}
{% tab title="AWS" %}
<pre class="language-yaml"><code class="lang-yaml"># The AWS region to deploy to.
region: eu-west-1 

# The name of the RDS instance to create
<strong>rds_name: zenmlserver
</strong>
<strong># Name of RDS database to create.
</strong>db_name: zenmlserver

# Type of RDS database to create.
db_type: mysql

# Version of RDS database to create.
db_version: 5.7.38

# Instance class of RDS database to create.
db_instance_class: db.t3.micro

# Allocated storage of RDS database to create.
db_allocated_storage: 5
</code></pre>

The `database_username` and `database_password` from the general config is used to set those variables for the AWS RDS instance.
{% endtab %}

{% tab title="GCP" %}
<pre class="language-yaml"><code class="lang-yaml"># The project in GCP to deploy the server in.
project_id: 

<strong># The GCP region to deploy to.
</strong>region: europe-west3

# The name of the CloudSQL instance to create.
cloudsql_name: zenmlserver

# Name of CloudSQL database to create.
db_name: zenmlserver

# Instance class of CloudSQL database to create.
db_instance_tier: db-n1-standard-1

# Allocated storage of CloudSQL database, in GB, to create.
db_disk_size: 10

# Whether or not to enable the Secrets Manager API. Disable this if you
# don't have ListServices permissions on the project.
enable_secrets_manager_api: true
</code></pre>

* The `project_id` is required to be set.
* The `database_username` and `database_password` from the general config is used to set those variables for the CloudSQL instance.
* SSL is disabled by default on the database and the option to enable it is coming soon!
{% endtab %}

{% tab title="Azure" %}
```yaml
# The Azure resource_group to deploy to.
resource_group: zenml

# The name of the Flexible MySQL instance to create.
db_instance_name: zenmlserver

# Name of RDS database to create.
db_name: zenmlserver

# Version of MySQL database to create.
db_version: 5.7

# The sku_name for the database resource.
db_sku_name: B_Standard_B1s

# Allocated storage of MySQL database to create.
db_disk_size: 20
```

The `database_username` and `database_password` from the general config is used to set those variables for the Azure Flexible MySQL server.
{% endtab %}
{% endtabs %}

## Connecting to deployed ZenML

Once ZenML is deployed, one or multiple users can connect to it with the `zenml connect` command.

```bash
zenml connect
```

{% hint style="info" %}
If no arguments are supplied, ZenML will attempt to connect to the last ZenML server deployed from the local host using the `zenml deploy` command:
{% endhint %}

In order to connect to a specific ZenML server, you can either pass the configuration as command line arguments or as a YAML file:

```bash
zenml connect --url=https://zenml.example.com:8080 --username=admin --no-verify-ssl
```

or

```bash
zenml connect --config=/path/to/zenml_server_config.yaml
```

The YAML file should have the following structure when connecting to a ZenML server:

```yaml
# The URL of the ZenML server
url:

# The username and password to use for authentication
username:
password:

# Either a boolean, in which case it controls whether the server's TLS 
# certificate is verified, or a string, in which case it must be a path 
# to a CA certificate bundle to use or the CA bundle value itself
verify_ssl: 
```

Here is an example of a ZenML server YAML configuration file:

```yaml
url: https://ac8ef63af203226194a7725ee71d85a-7635928635.us-east-1.elb.amazonaws.com/zenml
username: admin
password: Pa$$word123
verify_ssl: |
  -----BEGIN CERTIFICATE-----
  MIIDETCCAfmgAwIBAgIQYUmQg2LR/pHAMZb/vQwwXjANBgkqhkiG9w0BAQsFADAT
  MREwDwYDVQQDEwh6ZW5tbC1jYTAeFw0yMjA5MjYxMzI3NDhaFw0yMzA5MjYxMzI3
...
  ULnzA0JkRWRnFqH6uXeJo1KAVqtxn1xf8PYxx3NlNDr9wi8KKwARf2lwm6sH4mvq
  1aZ/0iYnGKCu7rLJzxeguliMf69E
  -----END CERTIFICATE-----
```

Both options can be combined, in which case the command line arguments will override the values in the YAML file. For example, it is possible and recommended that you supply the password only as a command line argument:

```bash
zenml connect --username zenml --password=Pa$$word --config=/path/to/zenml_server_config.yaml
```

To disconnect from the current ZenML server and revert to using the local default database, use the following command:

```bash
zenml disconnect
```

## How does it work?

Here's an architecture diagram that shows how the workflow looks like when you do `zenml deploy`.

![Running zenml deploy](../../.gitbook/assets/zenml_deploy.png)

The deploy CLI makes use of a "recipe" inside the `zenml-io/zenml` repository to deploy the server on the right cloud. Any configuration that you pass with the CLI, is sent to the recipe as input variables.

<!-- For scarf -->
<figure><img alt="ZenML Scarf" referrerpolicy="no-referrer-when-downgrade" src="https://static.scarf.sh/a.png?x-pxid=f0b4f458-0a54-4fcd-aa95-d5ee424815bc" /></figure>
