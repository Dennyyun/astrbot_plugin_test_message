from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult, CommandResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import astrbot.api.message_components as Comp


@register("my_group_plugin", "Denny", "一个群消息处理插件", "1.2.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""

    @filter.event_message_type(filter.EventMessageType.GROUP_MESSAGE)
    async def on_group_message(self, event: AstrMessageEvent):
        """群消息监听"""
        logger.info(f"收到事件类型: {type(event)}, 消息: {event.message_str}")
        """群消息监听回复"""
        group_id = event.get_group_id()  # 群号
        sender_name = event.get_sender_name()  # 发送者名字
        user_id = event.get_group_id()# 发送者qq号
        message = event.get_message_str()  # 消息内容
        logger.info(f"收到群{group_id}，{sender_name}的消息：{message}")

        if '你好' in message:
            yield CommandResult.message("你好呀！收到你的消息了！").at(sender_name,user_id)
        else:
            yield CommandResult.message("你好").at(sender_name,user_id)


    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command("helloworld")
    async def helloworld(self, event: AstrMessageEvent):
        """/helloword 指令回复"""  # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        user_name = event.get_sender_name()
        user_id = event.get_sender_id()  # 获取用户 ID
        message_str = event.message_str  # 用户发的纯文本消息字符串
        message_chain = event.get_messages()  # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        logger.info(message_chain)
        yield event.plain_result(f"Hello, {user_name}, 你发了 {message_str}!哈哈哈哈@{user_name}")  # 发送一条纯文本消息
