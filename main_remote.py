import asyncio
import traceback

from mcp_client import MCPClient


def init_client() -> MCPClient:
    """创建客户端实例"""
    client = MCPClient(server_name="weather", server_command="uvx", server_args=["darcycui-mcp"])
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
