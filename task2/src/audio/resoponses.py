wrong_format = {
    400: {
        "description": "Не верный формат записи",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Убедитесь, что загружаете файл в формате .wav"
                }
            }
        },
    }
}

no_file = {
    400: {
        "description": "Файл не найден",
        "content": {
            "application/json": {
                "example": {"detail": "У нас нет такого файла :("}
            }
        },
    }
}
