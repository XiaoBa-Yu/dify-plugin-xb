from typing import Any
from openai import OpenAI

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class TranslateProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        """
        验证 OpenAI API Key 有效性
        """

        try:
            # 使用轻量级请求验证密钥
            client = OpenAI(api_key=credentials.get("openai_api_key"))
            client.models.list()
            pass
        except Exception as e:
            raise ToolProviderCredentialValidationError(
                "Invalid API key or connection failed"
            )
