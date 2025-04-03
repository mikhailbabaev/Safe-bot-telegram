import os
import uuid
from yookassa import Webhook, WebhookRequest

# Получаем параметры из переменных окружения
shop_id = os.getenv("SHOP_ID")  # shopId
secret_key = os.getenv("SECRET_KEY")  # secretKey
ngrok_url = "https://3e7c-57-129-37-36.ngrok-free.app/webhook"  # URL для получения уведомлений от Юкассы

# Регистрация вебхука
def register_webhook():
    # Создаем объект с параметрами для вебхука
    params = {
        "event": "payment.succeeded",  # Уведомление о успешном платеже
        "url": ngrok_url  # Указание URL вебхука
    }

    try:
        # Создаем объект WebhookRequest с переданными параметрами
        response = Webhook.add(params)  # Используем метод add для регистрации вебхука
        print("Вебхук успешно зарегистрирован:", response)
    except Exception as e:
        print(f"Ошибка при регистрации вебхука: {e}")

if __name__ == "__main__":
    register_webhook()
