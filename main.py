from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import astrbot.api.message_components as Comp
import python_script

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
        """群消息监听回复 """
        logger.info(f"收到事件类型: {type(event)}, 消息: {event.message_str}")

        group_id = event.get_group_id()  # 群号
        sender_name = event.get_sender_name()  # 发送者名字
        user_id = event.get_group_id()  # 发送者qq号
        message = event.get_message_str()  # 消息内容
        logger.info(f"收到群{group_id}，{sender_name}的消息：{message}")
        if '你好' in message:
            yield event.chain_result([
                Comp.Plain("你好呀！收到你的消息了！"), Comp.At(qq=user_id)])
        elif "淘宝搜索："in message:
            const_key = message.split("淘宝搜索：")[1]
            result = python_script.taobao.main(const_key)
            yield event.chain_result([Comp.Plain(result), Comp.At(qq=user_id)])
        else:
            yield event.chain_result([Comp.Plain("哈哈哈"), Comp.At(qq=user_id)])
