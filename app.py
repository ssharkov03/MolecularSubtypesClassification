import asyncio
import logging

import tempfile

from aiogram.types import ContentType
from aiogram.utils.exceptions import FileIsTooBig

from config import TOKEN, HELP_PIC_PATH

from keyboards import help_button

from cancerTypingAlgo import cancerTypeDetection

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters import Command, Text


# Bot setting
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

# ================ Handlers =======================
# Start command handler
@dp.message_handler(Command("start"))
async def subscribe(message: types.Message):
    await message.answer("Рекомендуется прочтение инструкции перед использованием!\n", reply_markup=help_button)


# Input file handler
@dp.message_handler(content_types=ContentType.DOCUMENT)
async def files_handling(message: types.message):
    try:

        document_id = message.document.file_id
        file_name = message.document.file_name.split(".")
        type_of_document = file_name[-1]

        # Not correct type of data
        if type_of_document not in ['csv', 'txt', 'pickle']:

            await message.answer("Неверный тип файла! Прочитайте инструкцию!\n")

        else:

            file_info = await bot.get_file(document_id)
            await message.answer("Файл получен успешно\nНачат процесс предикации...\n")

            fi = file_info.file_path
            link_to_data = f'https://api.telegram.org/file/bot{TOKEN}/{fi}'

            # ML part
            analysis_result, analysis_comment = cancerTypeDetection(link_to_data, type_of_document)

            # Errors and risks handling
            if analysis_comment == "Error":
                await message.answer("Неверная структура файла! Прочитайте инструкцию!\n")

            elif analysis_comment == "Not dataframe":
                await message.answer("Загруженый .pickle файл не является pandas датафреймом!\n")

            else:
                await message.answer("Обработка результатов...\n")

                if analysis_comment[:4] == "Risk":
                    await message.answer(f"ВНИМАНИЕ!\nСоотношение количества полученных признаков к признакам, на которых обучалась модель сооставляет {float(analysis_comment.split()[-1])*100:0.6f}%.\nЕсть риск снижения точности предсказаний.\n")

                # Result processing
                res_file = tempfile.NamedTemporaryFile(suffix='.csv', prefix=f'prediction_for_{file_name[0]}__', delete=False)
                path_to_res_file = res_file.name
                analysis_result.to_csv(res_file, encoding='cp1251')
                await message.answer_document(document=open(path_to_res_file, "rb"))
                res_file.close()

    # In case file is too big
    except FileIsTooBig:
        await message.answer("Слишком большой файл...\n")


# Instruction description
@dp.message_handler(Text(equals=["Инструкция"]))
async def help_function(message: types.Message):
    text = """
Чтобы получить предсказание подтипа опухоли, отправьте боту файл содержащий геномы и данные о пораженных лимфоузлах пациентов.

Поддерживаемые типы входных файлов: *.csv | *.pickle | *.txt

После работы алгоритма вы получите файл формата .csv с предсказаниями.

Внутри входного файла должна быть следующая структура: 
"""
    await message.answer(text)
    await message.answer_photo(open(HELP_PIC_PATH, 'rb'))


# Start bot
async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")
