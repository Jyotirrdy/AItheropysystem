from ai_therapy_system import AITherapySystem


def test_detects_crisis_language():
    bot = AITherapySystem()
    response = bot.respond("I want to kill myself")
    assert "988" in response


def test_emotion_response():
    bot = AITherapySystem()
    response = bot.respond("I am so anxious and overwhelmed")
    assert "feeling anxious" in response


def test_default_response():
    bot = AITherapySystem()
    response = bot.respond("I cooked pasta")
    assert "What has your day felt like emotionally" in response
