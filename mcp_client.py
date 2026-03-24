import asyncio
import json
import traceback
from typing import Optional, Any

from mcp import ClientSession, StdioServerParameters, stdio_client


class MCPClient:
    def __init__(self, server_name: str, server_command: str, server_args: list):
        """
        初始化 MCP 客户端
        """
        self.server_name = server_name
        self.server_command = server_command
        self.server_args = server_args
        self.session: Optional[ClientSession] = None
        self.tools_cache: list[dict] = []
        self._stdio_transport = None
        self._read_stream = None
        self._write_stream = None

    async def connect(self):
        """连接到 MCP Server"""
        print(f"命令: {self.server_command}")
        print(f"参数: {self.server_args}")

        try:
            # 创建 ServerParameters
            server_params = StdioServerParameters(
                command=self.server_command,
                args=self.server_args
            )
            self._stdio_transport = stdio_client(server_params)
            read_write = await self._stdio_transport.__aenter__()
            self._read_stream, self._write_stream = read_write
            self.session = ClientSession(self._read_stream, self._write_stream)
            await self.session.__aenter__()
            await self.session.initialize()
            print("[MCP Client] ✓ 成功连接到 MCP 服务器")

            tools_response = await self.session.list_tools()
            self.tools_cache = [tool.model_dump() for tool in tools_response.tools]
            print("[MCP Client] 获取到Tools列表:", self.tools_cache)
            self.tools_cache = [tool.model_dump() for tool in tools_response.tools]


        except Exception as e:
            print(f"❌ 连接到 MCP 服务器失败: {e}")
            traceback.print_exc()
            raise

    async def disconnect(self):
        """断开 MCP Server"""
        if self.session:
            try:
                await self.session.__aexit__(None, None, None)
            except Exception as e:
                print(f"关闭 session 时出错：{e}")
            finally:
                self.session = None

        if self._stdio_transport:
            try:
                await self._stdio_transport.__aexit__(None, None, None)
            except Exception as e:
                print(f"关闭 stdio_transport 时出错：{e}")
            finally:
                self._stdio_transport = None
                self._read_stream = None
                self._write_stream = None

    async def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> str:
        """
        调用 MCP Server 的工具
        :param tool_name: 工具名称
        :param arguments: 工具参数
        :return: 工具执行结果
        """
        try:
            print(f"[MCP Client] {self.server_name} call tool {tool_name} with args: {arguments}")
            if not self.session:
                raise Exception(f"[MCP Client] {self.server_name} not connected")
            # result = await self.session.call_tool(tool_name, arguments)
            # 添加超时控制
            result = await asyncio.wait_for(
                self.session.call_tool(tool_name, arguments),
                timeout=50
            )
            print(f"[MCP Client] Got result from {self.server_name}/{tool_name}")
            if result.content:
                content = result.content[0]
                if hasattr(content, 'text'):
                    print(f"[MCP Client] Result text: {content.text[:200]}...")
                    return content.text
                elif isinstance(content, dict):
                    return json.dumps(content)
                else:
                    return str(content)
            return f"[MCP Client] {self.server_name} call tool {tool_name} SUCCESS"
        except Exception as e:
            error_message = f"[MCP Client] {self.server_name} call tool {tool_name} error: {e}"
            print(f"{error_message}")
            return error_message
