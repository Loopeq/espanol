from aiogram import Bot
from aiogram.types import CallbackQuery, FSInputFile

from data.database import get_words, get_word_by_id, get_section, get_sections
from domain.keyboards.keyboards import inline_words_kb, inline_section_kb, inline_return_to_section_kb, \
    inline_delete_voice

from domain.utils.common import clip_id
from resources.strings import Strings
from text_to_speech.voice_request import get_voice


async def cmd_words(callback: CallbackQuery):
    section_id = clip_id(callback.data, "section")
    section = get_section(section_id)[0]
    words = get_words(section_id)
    if not words:
        await callback.message.edit_text(text=Strings.oops_message,
                                         reply_markup=inline_return_to_section_kb())
    else:
        await callback.message.edit_text(text=section['title'] + Strings.voice_info,
                                         reply_markup=inline_words_kb(words=words))
    await callback.answer()

async def cmd_voice(callback: CallbackQuery, bot: Bot):
    word_id = clip_id(callback.data, "word")
    current_word = get_word_by_id(word_id)[0]
    voice_path = get_voice(current_word["espanol"], word_id)
    v_inp = FSInputFile(path = voice_path)
    await bot.send_voice(chat_id=callback.from_user.id, voice=v_inp,
                         caption=current_word["espanol"], reply_markup=inline_delete_voice(word_id=word_id))
    await callback.answer()

async def cmd_return_to_words(callback: CallbackQuery):
    section_id = clip_id(callback.data, "return_to_words")
    section = get_section(section_id)[0]
    words = get_words(section_id)
    await callback.message.edit_text(section['title'] + Strings.voice_info,  reply_markup=inline_words_kb(words=words))
    await callback.answer()

async def cmd_delete_voice(callback: CallbackQuery):
    await callback.message.delete()

async def cmd_return_to_sections(callback: CallbackQuery):
    await callback.message.edit_text(text=Strings.available_sections, reply_markup=inline_section_kb(get_sections()))
