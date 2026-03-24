import asyncio
import traceback

from mcp_client import MCPClient

MCP_SERVER_FOLDER = r"D:\Projectss\AI\MCP\DarcyMCPServerLocal\src\darcycui_mcp"
MCP_SERVER_FILE = r"weather.py"

SERVER_COMMAND_LOCAL = "uv"
SERVER_ARGS_LOCAL = [
    "--directory",
    MCP_SERVER_FOLDER,
    "run",
    MCP_SERVER_FILE
]


def init_client() -> MCPClient:
    """创建客户端实例"""
    client = MCPClient(server_name="weather", server_command=SERVER_COMMAND_LOCAL, server_args=SERVER_ARGS_LOCAL)
    return client


async def run_client():
    """运行客户端"""
    client = init_client()
    connection_successful = False
    try:
        print("连接 MCP 服务器...")
        await client.connect()
        connection_successful = True
        print("调用工具...")
        result = await client.call_tool("get_forecast", {"city": "上海"})
        print("工具结果:", result)
    except KeyboardInterrupt:
        print("\n用户中断")
    except asyncio.TimeoutError:
        print("⚠️ 工具调用超时")
        traceback.print_exc()
    except Exception as e:
        print(f"运行过程中出错: {e}")
        traceback.print_exc()
    finally:
        # 确保断开连接
        if connection_successful:
            print("断开连接...")
            await client.disconnect()
        else:
            print("连接未成功建立，跳过断开连接步骤")


if __name__ == "__main__":
    asyncio.run(run_client())
