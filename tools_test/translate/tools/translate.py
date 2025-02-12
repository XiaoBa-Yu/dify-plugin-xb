from collections.abc import Generator
from typing import Any
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from markitdown import MarkItDown
from openai import OpenAI


class TranslateTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        # 获取文件元数据
        file_blob = tool_parameters.get("files")

        try:
            base_url = tool_parameters.get("domain") or "http://localhost:5001"
            file_url = base_url + file_blob.url

            # 检查是否有 model 参数
            if tool_parameters.get("model"):
                if not self.runtime.credentials.get("openai_api_key"):
                    raise ValueError("openai_api_key is required for OpenAI model")
                client = OpenAI(
                    api_key=self.runtime.credentials["openai_api_key"],
                    base_url=self.runtime.credentials.get("openai_base_url", None),
                )
                md = MarkItDown(
                    llm_client=client, llm_model=tool_parameters.get("model")
                )
            else:
                md = MarkItDown()

            # 元数据只包含url 直接从URL转换
            md_result = md.convert(file_url)

            yield self.create_text_message("markdown转换成功")
            yield self.create_blob_message(
                blob=md_result.text_content, meta={"mime_type": "text/markdown"}
            )

        except Exception as e:
            error_msg = f"转换错误: {str(e)}"
            # 返回错误信息
            yield self.create_text_message(error_msg)
