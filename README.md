## sentinel
Sentinel is an OpenID Connect proxy for the CLI to transparently connect to endpoints behind an Identity Aware Proxy.

In [Zero Trust Networks](https://en.wikipedia.org/wiki/Zero_trust_security_model) Identity Aware Proxies (like [oauth2-proxy](https://oauth2-proxy.github.io/oauth2-proxy/), [oathkeeper](https://github.com/ory/oathkeeper)  or [Google IAP](https://cloud.google.com/iap)) are often used to secure endpoints using OpenID Connect.
Having that makes it really hard to work with endpoints in this network via CLI.
This is where sentinel kicks in. Sentinel starts a HTTP proxy on your local machine, handles the OpenID Connect handshake with your Identity Provider and injects your personal access token to the requests in your network.

### usage
```shell script
sentinel connect curl http://httpbin.org/bearer
```

or simply

```shell script
sentinel connect bash
```

### installation

#### build from source
- Check out GIT repository
- install [pyinstaller](https://www.pyinstaller.org/)
- `pyinstaller --onefile sentinel.py`

### configuration
Use `sentinel configure` to interactively configure your sentinel.

The configuration is stored in your home directory as JSON format in `~/.sentinel/config`.
You can also just modify this file.

#### options
field | description | default
--- | --- | ---
client_id | OIDC client id  | 
client_secret | OIDC client secret  | 
issuer | Issuer to authorize against  | 
allowed_hosts | hostnames of your network that are secured via OpenID Connect and where access token should be sent to | 
scopes | OIDC scopes to request  | ["openid"]
callback_port | port where the OIDC callback is listening on | 8099
proxy_port | port where the proxy is listening on when starting standalone | 8099
proxy_connect_port_start | start of port range where the proxy is listening on when using connect | 8000
proxy_connect_port_end | end of port range where the proxy is listening on when using connect | 8098

### working with ssl
Behind the scene sentinel is using [mitmproxy](https://docs.mitmproxy.org/stable/concepts-certificates/) which supports SSL interception:
[https://docs.mitmproxy.org/stable/concepts-certificates](https://docs.mitmproxy.org/stable/concepts-certificates/)

On ubuntu for example:
```shell script
sudo openssl x509 -in  ~/.mitmproxy/mitmproxy-ca-cert.pem -inform PEM -out /usr/share/ca-certificates/mitmproxy-ca-cert.crt
sudo dpkg-reconfigure ca-certificates
```

### standalone proxy on fixed port
If you want to just start a permanent proxy on a fixed port, just use this:
```shell script
sentinel proxy
```

and then make the proxy available to your tool or system. E.g.:
```shell script
export http_proxy=http://localhost:8098
export https_proxy=http://localhost:8098
``` 