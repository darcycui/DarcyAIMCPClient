## 是什么
MCP协议的客户端，支持连接本地 MCP-Server，并调用 MCP-Server提供的工具。


## 有什么能力
1. 连接 本地 MCP-Server [DarcyMCPServer](https://github.com/darcycui/DarcyAIMCPServer)
2. 查询 DarcyMCPServer 提供的全部工具
3. 调用 DarcyMCPServer 提供的工具 get_forecast

## 怎么用
1. clone 这个项目
2. clone [DarcyMCPServer](https://github.com/darcycui/DarcyAIMCPServer)
3. 修改全局变量
   - [mcp_client.py](mcp_client.py) 中的 MCP_SERVER_FOLDER 为 DarcyMCPServer 的路径
4. 运行 [main.py](main.py)

## 运行结果
![运行结果](MCP-Client运行效果.png)

## 参考文档
[MCP官网 创建MCP客户端](https://modelcontextprotocol.io/docs/develop/build-client)

[快速上手：实现你的第一个 MCP Client](https://zhuanlan.zhihu.com/p/21166726702)

[用最简单的方式教你用Python搭建第一个MCP服务器](https://juejin.cn/post/7496341504849330214)
