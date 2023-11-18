from pydantic_settings import BaseSettings, SettingsConfigDict

from backend.models import ChainId


class Settings(BaseSettings):
    app_name: str = "Fomogotchi API"

    one_inch_devportal_api_key: str

    ethereum_node_url: str
    polygon_node_url: str
    arbitrum_node_url: str
    gnosis_node_url: str

    redis_host: str
    redis_port: int
    redis_password: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

node_urls = {
    ChainId.ETH: settings.ethereum_node_url,
    ChainId.POLYGON: settings.polygon_node_url,
    ChainId.ARBITRUM: settings.arbitrum_node_url,
    ChainId.GNOSIS: settings.gnosis_node_url,
}
