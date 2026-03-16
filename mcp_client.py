import asyncio
import traceback
from typing import Optional, Any
from mcp import ClientSession, StdioServerParameters, stdio_client
import subprocess

MCP_SERVER_FOLDER = r"D:\Projectss\AI\DarcyMCP\DarcyMCPServer"
MCP_SERVER_FILE = r"weather.py"


class MCPClient:
    def __init__(self):
        """
        初始化 MCP 客户端
        """
        self.server_command = "uv"
        self.server_args = [
            "--directory",
            MCP_SERVER_FOLDER,
            "run",
            MCP_SERVER_FILE
        ]
        self.session: Optional[ClientSession] = None
        self.stdio_context = None
        self.reader = None
        self.writer = None

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

            # 建立连接
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    # 初始化连接
                    await session.initialize()
                    print("✓ 成功连接到 MCP 服务器")
                    # 列出可用工具
                    print("\n正在列出可用工具...")
                    tools = await session.list_tools()
                    print("Tools列表:", tools)
                    # 调用工具
                    print("\n正在调用 get_forecast...")
                    result = await session.call_tool("get_forecast", {"city": "北京"})
                    print(f"调用结果: {result}")


        except Exception as e:
            print(f"❌ 连接到 MCP 服务器失败: {e}")
            traceback.print_exc()
            raise
