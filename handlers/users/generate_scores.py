import datetime
from PIL import Image, ImageDraw, ImageFont
from aiogram import Router, F, types

from loader import db

router = Router()


async def generate_participants_image(participants: list, test_id: int, test_name: str = "") -> str:
    width, height = 1000, 60 + len(participants) * 40 + 50
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    # Font sozlamalari (agar sizda yo'q bo'lsa, ttf fayl yo'lini to'g'rilang)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
        header_font = ImageFont.truetype("arial.ttf", 26)
    except:
        font = ImageFont.load_default()
        header_font = font

    y = 20
    draw.text((width // 2 - 200, y), f"{test_id}-sonli \"{test_name}\" test natijalari", font=header_font, fill="black")
    y += 40
    draw.text((50, y), "T/r  Ismi Familiyasi               Ball   Foiz    Sana        Vaqt", font=font, fill="black")
    y += 10

    for i, row in enumerate(participants, 1):
        name = row["full_name"]
        score = row["score"]
        percent = row["percent"]
        dt: datetime.datetime = row["created_at"]
        date_str = dt.strftime("%Y-%m-%d")
        time_str = dt.strftime("%H:%M:%S")

        line = f"{i:<4} {name:<25} {score:<6} {percent:<6} {date_str} {time_str}"
        y += 30
        draw.text((50, y), line, font=font, fill="black")

    file_path = f"/tmp/test_{test_id}_participants.jpg"
    image.save(file_path, "JPEG")
    return file_path


@router.message(F.text.startswith("natija") & F.text.endswith("jpg"))
async def send_test_results_image(message: types.Message):
    try:
        test_id = int(message.text.split()[1])
    except (IndexError, ValueError):
        await message.answer("❌ Format noto‘g‘ri. Masalan: `natija 44 jpg`")
        return

    participants = await db.get_test_results(code=test_id)

    if not participants:
        await message.answer("❌ Bu testga hali hech kim qatnashmagan.")
        return

    image_path = await generate_participants_image(participants, test_id, test_name="Full_Math")
    await message.answer_photo(types.FSInputFile(image_path), caption=f"{test_id}-sonli test natijalari")
