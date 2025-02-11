from collections.abc import Generator
from typing import Any
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from markitdown import MarkItDown
from base64 import b64decode

class TranslateTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        # 获取文件元数据
        file_blob = tool_parameters.get('files')
        
        try:   
            # base_url = tool_parameters.get("mode", "")
            base_url = 'http://localhost:5001'
            file_url = base_url + file_blob.url         
            md = MarkItDown()
            # 元数据只包含url 直接从URL转换
            md_result = md.convert(file_url)
               
            yield self.create_text_message('markdown转换成功')
            yield self.create_blob_message(
                blob=md_result.text_content, meta={"mime_type": "text/markdown"}
            )
        
        except Exception as e:
            error_msg = f"转换错误: {str(e)}"
            # 返回错误信息
            yield self.create_text_message(error_msg)
            yield self.create_json_message({"error": error_msg})
            yield self.create_stream_variable_message(
                variable_name="error",
                variable_value=error_msg
            )