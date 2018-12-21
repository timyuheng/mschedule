from aiohttp import web
import zerorpc


class Web:
    def __init__(self):
        self.app = web.Application()
        self.app.add_routes([
            web.get('/task/agents', self.agentshandler),
            web.post("/task", self.taskhandler)

        ])

        # rpc client TODO 以后实现重连
        self.client = zerorpc.Client()
        self.client.connect("tcp://127.0.0.1:9000")

    def start(self):
        web.run_app(self.app, host='0.0.0.0', port=9900)

    async def agentshandler(self, request: web.Request):
        print(request)
        print(type(request))
        txt = self.client.get_agents()
        return web.json_response(txt)

    async def taskhandler(self, request: web.Request):
        j = await request.json()  # 获取请求的json内容
        print(j, '-------------')
        txt = self.client.add_task(j)  # j为字典
        return web.json_response(txt, status=201)
