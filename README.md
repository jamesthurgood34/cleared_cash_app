# Cleared Cash App
This repo contains a simple Streamlit app that accepts a CSV export from [Studio Ninja's](https://www.studioninja.co/) payment tab and aggregates it to calculate the value of deposits on the books. The aim of the app is to let you know, as simply as possible, how much "cleared cash" you have.

## Why this app is needed
It's often the case for businesses that take bookings upfront, like wedding photography, to collect deposits 1–2 years in advance. At first, this might seem great, as your bank balance rises with each booking. However, it's important to remember that the deposit is for future work, not yet completed. While the deposit is typically non-refundable, there may be circumstances where you have to return it. For this reason, it’s prudent to track your "cleared funds," i.e., your bank balance minus the total of your deposits.

## Running the app

### With Python
Clone this repo, install the `requirement.txt` and run

```bash
streamlit run app.py
```

### Building the container
I needed this app to run on an ARM host, so I containerized it.

For convenience, I created a `build_and_push.sh` script. You'll notice that I run a local Docker registry on my home network, so the host and port of the registry must be specified at build time.

Since this local registry is not configured with HTTPS, you'll encounter the following error if you use the default settings:

> http: server gave HTTP response to HTTPS client

To resolve this, I first updated `/etc/docker/daemon.json` with:

```json
{
     ["<HOSTNAME>:<PORT>"]
}
```

And then as I am using buildx you also need to create a new new builder instance using a custom config.

Create a file called `config.toml` and add

```toml
[registry."<HOSTNAME>:<PORT>"]
  http = true
```

and create the new builder

```bash
docker buildx create --driver-opt network=host --use --config config.toml --name <name>
```

you can then use this builder by running

```bash
./build_and_push.sh
```