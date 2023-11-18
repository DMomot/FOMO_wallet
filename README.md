
# FOMO Wallet

It ain't scam if it ain't a financial advice!


## Run

1. Deploy:
    * `./scripts/deploy`. Orc CI/CD goes brrr...
2. Open UI in browser:
    * If straight: `xdg-open https://fomo-wallet.duckdns.org`
    * If creative: `open https://fomo-wallet.duckdns.org`
3. Query API:
    * `curl https://fomo-wallet.duckdns.org/api/`
    * `curl https://fomo-wallet.duckdns.org/api/ping`


## `/dev/random`

1. What added to the standard `nginx.conf`?
    * `git diff -w fec605d -- nginx/`
2. IaaR: Infrastructure as a `README.md`
    * [How to install Nginx on Ubuntu 20.04](https://community.hetzner.com/tutorials/how-to-install-nginx-on-ubuntu-20-04)
    * [Add SSL Certificate with Lets Encrypt to Nginx on Ubuntu 20.04](https://community.hetzner.com/tutorials/add-ssl-certificate-with-lets-encrypt-to-nginx-on-ubuntu-20-04)
    * [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
