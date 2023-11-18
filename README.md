
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

1. Q: What added to the standard `nginx.conf`?
    * A: `git diff -w fec605d -- nginx/`
