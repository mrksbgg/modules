# Name: DND
# Description: DND (Do Not Disturb) :
# -> Предотвращает отправку людьми вам нежелательных личных сообщений.
# -> Предотвращает беспокойство, когда вы недоступны.\n
# Commands :
# Author: HitaloSama
# Переводчик на русский: nixend
# Commands:
# .unafk   | .afk     | .afknogroup | .afknopm | .afknotif
# .afkrate | .allow   | .block      | .deny    | .pm      
# .pmlimit | .pmnotif | .report     | .unblock
# ---------------------------------------------------------------------------------


#    Friendly Telegram (telegram userbot)
#    By Magical Unicorn (based on official Anti PM & AFK Friendly Telegram modules)
#    Copyright (C) 2020 Magical Unicorn

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Перевел на русский @nixend

from .. import loader, utils

import logging
import datetime
import time

from telethon import functions, types

logger = logging.getLogger(__name__)


@loader.tds
class DoNotDisturbMod(loader.Module):
    """
    DND (Do Not Disturb) :
    -> Предотвращает отправку людьми вам нежелательных личных сообщений.
    -> Предотвращает беспокойство, когда вы недоступны.\n
    Автор: HitaloSama
    Переводчик: nixend\n
    Команды:

    """
    strings = {
        "name": "DND",
        "afk": "<b><emoji document_id=5242500556819274882>⛔️</emoji> I'm AFK right now (since</b> <i>{}</i> <b>ago).</b>",
        "afk_back": "<b><emoji document_id=5247224183326256799>👋</emoji> I'm goin' BACK !</b>",
        "afk_gone": "<b><emoji document_id=5242500556819274882>⛔️</emoji> I'm goin' AFK !</b>",
        "afk_no_group_off": "<b><emoji document_id=5386539642369614675>✅</emoji> AFK status message enabled for group chats.</b>",
        "afk_no_group_on": "<b><emoji document_id=5190498849440931467>❌</emoji> AFK status message disabled for group chats.</b>",
        "afk_no_pm_off": "<b><emoji document_id=5979027086612892618>🙋🏻‍♂️</emoji> AFK status message enabled for PMs.</b>",
        "afk_no_pm_on": "<b><emoji document_id=5976553640716930004>🙅🏻‍♂️</emoji> AFK status message disabled for PMs.</b>",
        "afk_notif_off": "<b><emoji document_id=5974558538213625534>🔈</emoji> Notifications are now disabled during AFK time.</b>",
        "afk_notif_on": "<b><emoji document_id=5976746905655316100>🔊</emoji> Notifications are now enabled during AFK time.</b>",
        "afk_rate_limit_off": "<b><emoji document_id=5465300082628763143>💬</emoji> AFK status message rate limit disabled.</b>",
        "afk_rate_limit_on": (
            "<b><emoji document_id=5188391205909569136>✅</emoji> AFK status message rate limit enabled.</b>"
            "\n\n<b><emoji document_id=5467910507916697142>💢</emoji>  One AFK status message max will be sent per chat.</b>"
        ),
        "afk_reason": (
            "<b><emoji document_id=5242500556819274882>⛔️</emoji> I'm AFK right now (since {} ago).</b>" "\n\n<b>Reason :</b> <i>{}</i>"
        ),
        "arg_on_off": "<b><emoji document_id=5203980348056149676>👨‍💻</emoji> Argument must be <code>off</code> or <code>on</code>!</b>",
        "pm_off": (
            "<b><emoji document_id=5246885387716011812>🫥</emoji> Automatic answer for denied PMs disabled."
            "\n\n<emoji document_id=5388929052935462187>😎</emoji> Users are now free to PM !</b>"
        ),
        "pm_on": "<b><emoji document_id=5381855971943389791>🤐</emoji> An automatic answer is now sent for denied PMs.</b>",
        "pm_allowed": "<b></b><emoji document_id=5391210243210353922>👍</emoji> I have allowed</b> <a href='tg://user?id={}'>you</a> <b>to PM now.</b>",
        "pm_blocked": (
            "<b><emoji document_id=5206432422194849059>🔒</emoji> I don't want any PM from</b> <a href='tg://user?id={}'>you</a>, "
            "<b>so you have been blocked !</b>"
        ),
        "pm_denied": "<b><emoji document_id=5246885387716011812>🫥</emoji> I have denied</b> <a href='tg://user?id={}'>you</a> <b>to PM now.</b>",
        "pm_go_away": (
            "<emoji document_id=5391042881219731337>👀</emoji> Hey there! Unfortunately, I don't accept private messages from strangers."
            "\n\n<emoji document_id=5226772700113935347>📞</emoji> Please contact me in a group, or <b>wait</b> for me to approve you."
        ),
        "pm_reported": "<b><emoji document_id=5465432711218863135>♨️</emoji> You just got reported to spam !</b>",
        "pm_limit_arg": "<b><emoji document_id=5203980348056149676>👨‍💻</emoji> Argument must be <code>off</code>, <code>on</code> or a number between 5 and 1000!</b>",
        "pm_limit_off": "<b><emoji document_id=5188391205909569136>✅</emoji> Not allowed users are now free to PM without be automatically blocked.</b>",
        "pm_limit_on": "<b><emoji document_id=5972201876773408053>🚫</emoji> Not allowed users are now blocked after {} PMs.</b>",
        "pm_limit_current": "<b><emoji document_id=5467890025217661107>‼️</emoji> Current limit is {}.</b>",
        "pm_limit_current_no": "<b><emoji document_id=5188391205909569136>✅</emoji> Automatic user blocking is currently disabled.</b>",
        "pm_limit_reset": "<b><emoji document_id=5465665476971471368>❌</emoji> Limit reseted to {}.</b>",
        "pm_limit_set": "<b><emoji document_id=5467890025217661107>‼️</emoji> Limit set to {}.</b>",
        "pm_notif_off": "<b><emoji document_id=5974558538213625534>🔇</emoji> Notifications from denied PMs are now disabled.</b>",
        "pm_notif_on": "<b><emoji document_id=5976746905655316100>🔊</emoji> Notifications from denied PMs are now enabled.</b>",
        "pm_triggered": (
            "Hey! I don't appreciate you barging into my PM like this !"
            "\nDid you even ask me for approving you to PM ? No ?"
            "\nGoodbye then."
            "\n\nPS: You've been reported as spam."
        ),
        "pm_unblocked": (
            "<b><emoji document_id=5247224183326256799>👌</emoji> Alright fine! I'll forgive them this time. PM has been unblocked for</b> "
            "<a href='tg://user?id={}'>this user</a>."
        ),
        "unknow": (
            "An unknow problem as occured."
            "\n\nPlease report problem with logs on "
            "<a href='https://github.com/LegendaryUnicorn/FTG-Unofficial-Modules'>Github</a>."
        ),
        "who_to_allow": "<b><emoji document_id=5368809197032971971>🤔</emoji> Who shall I allow to PM ?</b>",
        "who_to_block": "<b><emoji document_id=5368809197032971971>🤔</emoji> Specify who to block.</b>",
        "who_to_deny": "<b><emoji document_id=5368809197032971971>🤔</emoji> Who shall I deny to PM ?</b>",
        "who_to_report": "<b><emoji document_id=5368809197032971971>🤔</emoji> Who shall I report ?</b>",
        "who_to_unblock": "<b><emoji document_id=5368809197032971971>🤔</emoji> Specify who to unblock.</b>",
    }

    strings_ru = {
        "name": "DND",
        "afk": "<b><emoji document_id=5242500556819274882>⛔️</emoji> Я сейчас не в сети (был </b> <i>{}</i> <b> назад).</b>",
        "afk_back": "<b><emoji document_id=5247224183326256799>👋</emoji> Я снова в сети</b>",
        "afk_gone": "<b><emoji document_id=5242500556819274882>⛔️</emoji> Я пока не в сети</b>",
        "afk_no_group_off": "<b><emoji document_id=5386539642369614675>✅</emoji> AFK статус был включен в группах</b>",
        "afk_no_group_on": "<b><emoji document_id=5190498849440931467>❌</emoji> AFK статус был отключен в группах</b>",
        "afk_no_pm_off": "<b><emoji document_id=5979027086612892618>🙋🏻‍♂️</emoji> AFK статус был включен в личных сообщениях.</b>",
        "afk_no_pm_on": "<b><emoji document_id=5976553640716930004>🙅🏻‍♂️</emoji> AFK статус был отключен в личных сообщениях.</b>",
        "afk_notif_off": "<b><emoji document_id=5974558538213625534>🔈</emoji> Уведомления теперь отключены во время AFK.</b>",
        "afk_notif_on": "<b><emoji document_id=5976746905655316100>🔊</emoji> Уведомления теперь включены во время AFK.</b>",
        "afk_rate_limit_off": "<b><emoji document_id=5465300082628763143>💬</emoji> Ограничение сообщений о статусе AFK отключено.</b>",
        "afk_rate_limit_on": (
            "<b><emoji document_id=5188391205909569136>✅</emoji> Ограничение сообщений о статусе AFK включено.</b>"
            "\n\n<b><emoji document_id=5467910507916697142>💢</emoji>  На каждый чат будет отправлено максимум одно сообщение о статусе AFK.</b>"
        ),
        "afk_reason": (
            "<b><emoji document_id=5242500556819274882>⛔️</emoji> Я сейчас не в сети (был в сети {} назад).</b>" "\n\n<b>Причина:</b> <i>{}</i>"
        ),
        "arg_on_off": "<b><emoji document_id=5203980348056149676>👨‍💻</emoji> Аргумент должен быть <code>on</code> или <code>off</code>!</b>",
        "pm_off": (
            "<b><emoji document_id=5246885387716011812>🫥</emoji> Автоматический ответ на отклоненное личное сообщение отключен."
            "\n\n<emoji document_id=5388929052935462187>😎</emoji> Пользователи теперь могут свободно писать в личные сообщения!</b>"
        ),
        "pm_on": "<b><emoji document_id=5381855971943389791>🤐</emoji> Теперь для отказанных личных сообщений отправляется автоматический ответ.</b>",
        "pm_allowed": "<b></b><emoji document_id=5391210243210353922>👍</emoji> <a href='tg://user?id={}'>Вы</a> <b>были одобрены в личные сообщения.</b>",
        "pm_blocked": (
            "<b><emoji document_id=5206432422194849059>🔒</emoji> Я не хочу получать сообщения от </b> <a href='tg://user?id={}'>вас</a>, "
            "<b>поэтому вы были заблокированы!</b>"
        ),
        "pm_denied": "<b><emoji document_id=5246885387716011812>🫥</emoji> Я ограничил</b> <a href='tg://user?id={}'>вам</a> <b>личные сообщения в данный момент.</b>",
        "pm_go_away": (
            "<emoji document_id=5391042881219731337>👀</emoji> К сожалению, я не принимаю личные сообщения от незнакомых людей"
            "\n\n<emoji document_id=5226772700113935347>📞</emoji> Пожалуйста, свяжитесь со мной в группе или <b>подождите</b> пока я свяжусь с вами здесь."
        ),
        "pm_reported": "<b><emoji document_id=5465432711218863135>♨️</emoji> Вы получили жалобу за спам!</b>",
        "pm_limit_arg": "<b><emoji document_id=5203980348056149676>👨‍💻</emoji> Аргумент должен быть <code>on</code>, <code>off</code> или любое число от 5 до 1000!</b>",
        "pm_limit_off": "<b><emoji document_id=5188391205909569136>✅</emoji> Любые пользователи теперь могут свободно отправлять сообщения в личку без автоматической блокировки.</b>",
        "pm_limit_on": "<b><emoji document_id=5972201876773408053>🚫</emoji> Незнакомые пользователи теперь блокируются после {} сообщений</b>",
        "pm_limit_current": "<b><emoji document_id=5467890025217661107>‼️</emoji> Текущий лимит {}.</b>",
        "pm_limit_current_no": "<b><emoji document_id=5188391205909569136>✅</emoji> Автоматическая блокировка пользователей отключена.</b>",
        "pm_limit_reset": "<b><emoji document_id=5465665476971471368>❌</emoji> Лимит сброшен до {}.</b>",
        "pm_limit_set": "<b><emoji document_id=5467890025217661107>‼️</emoji> Установлен лимит в {} сообщений.</b>",
        "pm_notif_off": "<b><emoji document_id=5974558538213625534>🔇</emoji> Уведомления от заблокированных пользователей теперь отключены.</b>",
        "pm_notif_on": "<b><emoji document_id=5976746905655316100>🔊</emoji> Уведомления от заблокированных пользователей теперь включены.</b>",
        "pm_triggered": (
            "Мне не нравится, что ты игнорируешь просьбу не писать мне!"
            "\nПока!"
            "\n\nP. S. На вас была отправлена жалоба за спам)))"
        ),
        "pm_unblocked": (
            "<b><emoji document_id=5247224183326256799>👌</emoji> ЛС был разблокирован для</b> "
            "<a href='tg://user?id={}'>этого человека</a>."
        ),
        "unknow": (
            "Возникла неизвестная проблема."
            "\n\nПожалуйста, сообщите о проблеме с регистрацией на"
            "<a href='https://github.com/LegendaryUnicorn/FTG-Unofficial-Modules'>Github</a>."
        ),
        "who_to_allow": "<b><emoji document_id=5368809197032971971>🤔</emoji> Кому я должен разрешить писать в личку?</b>",
        "who_to_block": "<b><emoji document_id=5368809197032971971>🤔</emoji> Кого заблокировать то?</b>",
        "who_to_deny": "<b<emoji document_id=5368809197032971971>🤔</emoji> >Кому отозвать разрешение писать вам в личку?</b>",
        "who_to_report": "<b><emoji document_id=5368809197032971971>🤔</emoji> На кого я должен пожаловаться?</b>",
        "who_to_unblock": "<b><emoji document_id=5368809197032971971>🤔</emoji> Кого разблокировать то?</b>",
    }

    def __init__(self):
        self._me = None
        self.default_pm_limit = 50

    async def client_ready(self, client, db):
        self._db = db
        self._client = client
        self._me = await client.get_me(True)

    async def unafkcmd(self, message):
        """Удалить AFK статус\n"""
        self._db.set(__name__, "afk", False)
        self._db.set(__name__, "afk_gone", None)
        self._db.set(__name__, "afk_rate", [])
        await utils.answer(message, self.strings("afk_back", message))

    async def afkcmd(self, message):
        """
        [причина] - Запустить AFK статус.

        """
        if utils.get_args_raw(message):
            self._db.set(__name__, "afk", utils.get_args_raw(message))
        else:
            self._db.set(__name__, "afk", True)
        self._db.set(__name__, "afk_gone", time.time())
        self._db.set(__name__, "afk_rate", [])
        await utils.answer(message, self.strings("afk_gone", message))

    async def afknogroupcmd(self, message):
        """
        [off/on] - Включение/отключение оповещения о статусе AFK в группах.

        """
        if utils.get_args_raw(message):
            afknogroup_arg = utils.get_args_raw(message)
            if afknogroup_arg == "off":
                self._db.set(__name__, "afk_no_group", False)
                await utils.answer(message, self.strings("afk_no_group_off"))
            elif afknogroup_arg == "on":
                self._db.set(__name__, "afk_no_group", True)
                await utils.answer(message, self.strings("afk_no_group_on", message))
            else:
                await utils.answer(message, self.strings("arg_on_off", message))
        else:
            afknogroup_current = self._db.get(__name__, "afk_no_group")
            if afknogroup_current is None or afknogroup_current is False:
                self._db.set(__name__, "afk_no_group", True)
                await utils.answer(message, self.strings("afk_no_group_on", message))
            elif afknogroup_current is True:
                self._db.set(__name__, "afk_no_group", False)
                await utils.answer(message, self.strings("afk_no_group_off", message))
            else:
                await utils.answer(message, self.strings("unknow", message))

    async def afknopmcmd(self, message):
        """
        [off/on] - Включение/отключение оповещения статуса AFK в личке.

        """
        if utils.get_args_raw(message):
            afknopm_arg = utils.get_args_raw(message)
            if afknopm_arg == "off":
                self._db.set(__name__, "afk_no_pm", False)
                await utils.answer(message, self.strings("afk_no_pm_off", message))
            elif afknopm_arg == "on":
                self._db.set(__name__, "afk_no_pm", True)
                await utils.answer(message, self.strings("afk_no_pm_on", message))
            else:
                await utils.answer(message, self.strings("arg_on_off", message))
        else:
            afknopm_current = self._db.get(__name__, "afk_no_pm")
            if afknopm_current is None or afknopm_current is False:
                self._db.set(__name__, "afk_no_pm", True)
                await utils.answer(message, self.strings("afk_no_pm_on", message))
            elif afknopm_current is True:
                self._db.set(__name__, "afk_no_pm", False)
                await utils.answer(message, self.strings("afk_no_pm_off", message))
            else:
                await utils.answer(message, self.strings("unknow", message))

    async def afknotifcmd(self, message):
        """
        [on/off] - Включить/отключить уведомления во время AFK.

        """
        if utils.get_args_raw(message):
            afknotif_arg = utils.get_args_raw(message)
            if afknotif_arg == "off":
                self._db.set(__name__, "afk_notif", False)
                await utils.answer(message, self.strings("afk_notif_off", message))
            elif afknotif_arg == "on":
                self._db.set(__name__, "afk_notif", True)
                await utils.answer(message, self.strings("afk_notif_on", message))
            else:
                await utils.answer(message, self.strings("arg_on_off", message))
        else:
            afknotif_current = self._db.get(__name__, "afk_notif")
            if afknotif_current is None or afknotif_current is False:
                self._db.set(__name__, "afk_notif", True)
                await utils.answer(message, self.strings("afk_notif_on", message))
            elif afknotif_current is True:
                self._db.set(__name__, "afk_notif", False)
                await utils.answer(message, self.strings("afk_notif_off", message))
            else:
                await utils.answer(message, self.strings("unknow", message))

    async def afkratecmd(self, message):
        """
        [on/off] - Включить/отключить ограничение в одно сообщение о статусе AKF.

        """
        if utils.get_args_raw(message):
            afkrate_arg = utils.get_args_raw(message)
            if afkrate_arg == "off":
                self._db.set(__name__, "afk_rate_limit", False)
                await utils.answer(message, self.strings("afk_rate_limit_off", message))
            elif afkrate_arg == "on":
                self._db.set(__name__, "afk_rate_limit", True)
                await utils.answer(message, self.strings("afk_rate_limit_on", message))
            else:
                await utils.answer(message, self.strings("arg_on_off", message))
        else:
            afkrate_current = self._db.get(__name__, "afk_rate_limit")
            if afkrate_current is None or afkrate_current is False:
                self._db.set(__name__, "afk_rate_limit", True)
                await utils.answer(message, self.strings("afk_rate_limit_on", message))
            elif afkrate_current is True:
                self._db.set(__name__, "afk_rate_limit", False)
                await utils.answer(message, self.strings("afk_rate_limit_off", message))
            else:
                await utils.answer(message, self.strings("unknow", message))

    async def allowcmd(self, message):
        """Разрешить пользователю писать в лс.\n"""
        user = await utils.get_target(message)
        if not user:
            await utils.answer(message, self.strings("who_to_allow", message))
            return
        self._db.set(
            __name__,
            "allow",
            list(set(self._db.get(__name__, "allow", [])).union({user})),
        )
        await utils.answer(message, self.strings("pm_allowed", message).format(user))

    async def blockcmd(self, message):
        """Заблокировать пользователя в лс без репорта.\n"""
        user = await utils.get_target(message)
        if not user:
            await utils.answer(message, self.strings("who_to_block", message))
            return
        await message.client(functions.contacts.BlockRequest(user))
        await utils.answer(message, self.strings("pm_blocked", message).format(user))

    async def denycmd(self, message):
        """Запретить писать в лс без предупреждения.\n"""
        user = await utils.get_target(message)
        if not user:
            await utils.answer(message, self.strings("who_to_deny", message))
            return
        self._db.set(
            __name__,
            "allow",
            list(set(self._db.get(__name__, "allow", [])).difference({user})),
        )
        await utils.answer(message, self.strings("pm_denied", message).format(user))

    async def pmcmd(self, message):
        """
        [on/off] - Включить/отключить автоматический ответ для отклоненных личных сообщений.

        """
        if utils.get_args_raw(message):
            pm_arg = utils.get_args_raw(message)
            if pm_arg == "off":
                self._db.set(__name__, "pm", True)
                await utils.answer(message, self.strings("pm_off", message))
            elif pm_arg == "on":
                self._db.set(__name__, "pm", False)
                await utils.answer(message, self.strings("pm_on", message))
            else:
                await utils.answer(message, self.strings("arg_on_off", message))
        else:
            pm_current = self._db.get(__name__, "pm")
            if pm_current is None or pm_current is False:
                self._db.set(__name__, "pm", True)
                await utils.answer(message, self.strings("pm_off", message))
            elif pm_current is True:
                self._db.set(__name__, "pm", False)
                await utils.answer(message, self.strings("pm_on", message))
            else:
                await utils.answer(message, self.strings("unknow", message))

    async def pmlimitcmd(self, message):
        """
        [on/off/reset/(number)] - Установить максимальное количество сообщений в лс, прежде чем автоматически блокировать пользователя.

        """
        if utils.get_args_raw(message):
            pmlimit_arg = utils.get_args_raw(message)
            if pmlimit_arg == "off":
                self._db.set(__name__, "pm_limit", False)
                await utils.answer(message, self.strings("pm_limit_off", message))
                return
            elif pmlimit_arg == "on":
                self._db.set(__name__, "pm_limit", True)
                pmlimit_on = self.strings("pm_limit_on", message).format(
                    self.get_current_pm_limit()
                )
                await utils.answer(message, pmlimit_on)
                return
            elif pmlimit_arg == "reset":
                self._db.set(__name__, "pm_limit_max", self.default_pm_limit)
                pmlimit_reset = self.strings("pm_limit_reset", message).format(
                    self.get_current_pm_limit()
                )
                await utils.answer(message, pmlimit_reset)
                return
            else:
                try:
                    pmlimit_number = int(pmlimit_arg)
                    if pmlimit_number >= 5 and pmlimit_number <= 1000:
                        self._db.set(__name__, "pm_limit_max", pmlimit_number)
                        pmlimit_new = self.strings("pm_limit_set", message).format(
                            self.get_current_pm_limit()
                        )
                        await utils.answer(message, pmlimit_new)
                        return
                    else:
                        await utils.answer(
                            message, self.strings("pm_limit_arg", message)
                        )
                        return
                except ValueError:
                    await utils.answer(message, self.strings("pm_limit_arg", message))
                    return
            await utils.answer(message, self.strings("limit_arg", message))
        else:
            pmlimit = self._db.get(__name__, "pm_limit")
            if pmlimit is None or pmlimit is False:
                pmlimit_current = self.strings("pm_limit_current_no", message)
            elif pmlimit is True:
                pmlimit_current = self.strings("pm_limit_current", message).format(
                    self.get_current_pm_limit()
                )
            else:
                await utils.answer(message, self.strings("unknow", message))
                return
            await utils.answer(message, pmlimit_current)

    async def pmnotifcmd(self, message):
        """
        [on/off] - Включить/отключить уведомления от заблокированных пользователей.

        """
        if utils.get_args_raw(message):
            pmnotif_arg = utils.get_args_raw(message)
            if pmnotif_arg == "off":
                self._db.set(__name__, "pm_notif", False)
                await utils.answer(message, self.strings("pm_notif_off", message))
            elif pmnotif_arg == "on":
                self._db.set(__name__, "pm_notif", True)
                await utils.answer(message, self.strings("pm_notif_on", message))
            else:
                await utils.answer(message, self.strings("arg_on_off", message))
        else:
            pmnotif_current = self._db.get(__name__, "pm_notif")
            if pmnotif_current is None or pmnotif_current is False:
                self._db.set(__name__, "pm_notif", True)
                await utils.answer(message, self.strings("pm_notif_on", message))
            elif pmnotif_current is True:
                self._db.set(__name__, "pm_notif", False)
                await utils.answer(message, self.strings("pm_notif_off", message))
            else:
                await utils.answer(message, self.strings("unknow", message))

    async def reportcmd(self, message):
        """Пожаловаться на спам. Работает только в личных сообщениях.\n"""
        user = await utils.get_target(message)
        if not user:
            await utils.answer(message, self.strings("who_to_report", message))
            return
        self._db.set(
            __name__,
            "allow",
            list(set(self._db.get(__name__, "allow", [])).difference({user})),
        )
        if message.is_reply and isinstance(message.to_id, types.PeerChannel):
            await message.client(
                functions.messages.ReportRequest(
                    peer=message.chat_id,
                    id=[message.reply_to_msg_id],
                    reason=types.InputReportReasonSpam(),
                )
            )
        else:
            await message.client(
                functions.messages.ReportSpamRequest(peer=message.to_id)
            )
        await utils.answer(message, self.strings("pm_reported", message))

    async def unblockcmd(self, message):
        """Разблокировать пользователя в лс."""
        user = await utils.get_target(message)
        if not user:
            await utils.answer(message, self.strings("who_to_unblock"))
            return
        await message.client(functions.contacts.UnblockRequest(user))
        await utils.answer(message, self.strings("pm_unblocked", message).format(user))

    async def watcher(self, message):
        user = await utils.get_user(message)
        pm = self._db.get(__name__, "pm")
        if getattr(message.to_id, "user_id", None) == self._me.user_id and (
            pm is None or pm is False
        ):
            if (
                not user.is_self
                and not user.bot
                and not user.verified
                and not self.get_allowed(message.from_id)
            ):
                await utils.answer(message, self.strings("pm_go_away", message))
                if self._db.get(__name__, "pm_limit") is True:
                    pms = self._db.get(__name__, "pms", {})
                    pm_limit = self._db.get(__name__, "pm_limit_max")
                    pm_user = pms.get(message.from_id, 0)
                    if (
                        isinstance(pm_limit, int)
                        and pm_limit >= 5
                        and pm_limit <= 1000
                        and pm_user >= pm_limit
                    ):
                        await utils.answer(
                            message, self.strings("pm_triggered", message)
                        )
                        await message.client(
                            functions.contacts.BlockRequest(message.from_id)
                        )
                        await message.client(
                            functions.messages.ReportSpamRequest(peer=message.from_id)
                        )
                        del pms[message.from_id]
                        self._db.set(__name__, "pms", pms)
                    else:
                        self._db.set(
                            __name__,
                            "pms",
                            {**pms, message.from_id: pms.get(message.from_id, 0) + 1},
                        )
                pm_notif = self._db.get(__name__, "pm_notif")
                if pm_notif is None or pm_notif is False:
                    await message.client.send_read_acknowledge(message.chat_id)
                return
        if (
            message.mentioned
            or getattr(message.to_id, "user_id", None) == self._me.user_id
        ):
            afk_status = self._db.get(__name__, "afk")
            if user.is_self or user.bot or user.verified or afk_status is False:
                return
            if message.mentioned and self._db.get(__name__, "afk_no_group") is True:
                return
            afk_no_pm = self._db.get(__name__, "afk_no_pm")
            if (
                getattr(message.to_id, "user_id", None) == self._me.user_id
                and afk_no_pm is True
            ):
                return
            if self._db.get(__name__, "afk_rate_limit") is True:
                afk_rate = self._db.get(__name__, "afk_rate", [])
                if utils.get_chat_id(message) in afk_rate:
                    return
                else:
                    self._db.setdefault(__name__, {}).setdefault("afk_rate", []).append(
                        utils.get_chat_id(message)
                    )
                    self._db.save()
            now = datetime.datetime.now().replace(microsecond=0)
            gone = datetime.datetime.fromtimestamp(
                self._db.get(__name__, "afk_gone")
            ).replace(microsecond=0)
            diff = now - gone
            if afk_status is True:
                afk_message = self.strings("afk", message).format(diff)
            elif afk_status is not False:
                afk_message = self.strings("afk_reason", message).format(
                    diff, afk_status
                )
            await utils.answer(message, afk_message)
            afk_notif = self._db.get(__name__, "afk_notif")
            if afk_notif is None or afk_notif is False:
                await message.client.send_read_acknowledge(message.chat_id)

    def get_allowed(self, id):
        return id in self._db.get(__name__, "allow", [])

    def get_current_pm_limit(self):
        pm_limit = self._db.get(__name__, "pm_limit_max")
        if not isinstance(pm_limit, int) or pm_limit < 5 or pm_limit > 1000:
            pm_limit = self.default_pm_limit
            self._db.set(__name__, "pm_limit_max", pm_limit)
        return pm_limit
