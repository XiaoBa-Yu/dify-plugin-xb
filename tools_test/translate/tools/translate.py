from collections.abc import Generator
from typing import Any
from googletrans import Translator
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

class TranslateTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        # 获取query参数
        input_text = tool_parameters.get('query', '')
        
        try:
            translator = Translator()
            
            # 检测输入文本的语言
            detected = translator.detect(input_text)
            
            if detected.lang == 'en':
                # 如果是英文，翻译成中文
                result = translator.translate(input_text, dest='zh-cn').text
            else:
                # 如果不是英文，翻译成英文
                result = translator.translate(input_text, dest='en').text
            
            # 返回三个固定变量：files、text、json
            # 1. text 变量
            yield self.create_text_message(result)
    
            
        except Exception as e:
            error_msg = f"翻译错误: {str(e)}"
            # 返回错误信息
            yield self.create_text_message(error_msg)
            yield self.create_json_message({"error": error_msg})
            yield self.create_stream_variable_message(
                variable_name="error",
                variable_value=error_msg
            )