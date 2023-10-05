# Das sind alle Bibliotheken die für dieses Programm benötigt werden.
import gradio as gr
import python_weather
import asyncio


async def get_weather(city):
    """
    Die Funktion holt sich über eine Wetter-API (Application Programming Interface) die entsprechenden aktuellen
    Wetterinformationen zu der übergebenen Stadt und liefert diese zurück.

    :param city: Der Städtename, zu dem die Wetterinformationen zurückgegeben werden sollen

    :return: Gibt die aktuellen Wetterinformationen zu der spezifischen Stadt zurück
    """

    async with python_weather.Client(unit=python_weather.METRIC, locale=python_weather.Locale.GERMAN) as client:
        weather = await client.get(city)
    return f"Das aktuelle Wetter in {city} ist {weather.current.description} {weather.current.kind.emoji} " \
           f"und die aktuelle Temperatur beträgt {weather.current.temperature} Grad!"


def create_weather_response(city, intent):
    """
    Funktion, die die entsprechende Wetterinformation zu der Stadt zurückgibt oder eine Fehlermeldung.

    :param city: Der Städtename, zu dem die Wetterinformationen zurückgegeben werden sollen. Wurde keine Stadt
    eingegeben, die in der Liste city_names zu finden ist, ist die Variable None

    :param intent: Die Variable ist True, wenn ein entsprechendes Wetter Schlagwort in der Anfrage gefunden wurde.
    Ansonsten ist die Variable False

    :return: Liefert die Wetterinformation oder eine entsprechende Fehlermeldung zurück
    """

    # Beinhaltet die Anfrage einen Städtenamen, der in der city_names Liste vorkommt?
    if city:
        # Ja, die Anfrage beinhaltet einen Städtenamen, der in der city_names Liste vorkommt
        # Beinhaltet die Anfrage ein gültiges Wetter Schlagwort, welches in der intents Liste vorkommt?
        if intent:
            # Ja, die Anfrage beinhaltet ein gültiges Wetter Schlagwort, welches in der intents Liste vorkommt
            # Rufe die Funktion get_weather auf und speichere das Ergebnis in der Variable answer
            answer = asyncio.run(get_weather(city))
        else:
            # Nein, die Anfrage beinhaltet kein gültiges Wetter Schlagwort, welches in der intents Liste vorkommt
            # Diese Antwort wird angezeigt, wenn kein gültiges Wetter Schlagwort in der Anfrage vorhanden ist
            answer = "Bitte geben Sie eine gültige Wetteranfrage an!"
    else:
        # Nein, die Anfrage beinhaltet keinen gültigen Städtenamen, der in der city_names Liste vorkommt
        # Diese Antwort wird angezeigt, wenn kein gültiger Städtenamen in der Anfrage vorhanden ist
        answer = "Bitte geben Sie eine spezifische Stadt in Ihrer Anfrage an!"

    # Gebe die definierte Antwort zurück
    return answer


def response(message, history):
    """
    Generiert die Antwort auf die Eingabe des Benutzers.

    :param message: Parameter, der die Benutzereingabe enthält. Das, was der Benutzer eingegeben hat, bevor er auf
    Submit drückt, steht in diesem Parameter

    :param history: Parameter, der die Chat-Historie enthält. Alles, was bereits eingegeben wurde, steht in diesem
    Parameter

    :return: Die Funktion gibt die generierte Antwort auf die Benutzereingabe zurück
    """

    # Liste mit allen Wörtern bei denen erkannt wird, dass der Benutzer*in etwas über das Wetter wissen will.
    intents = [
        'wetter',
        'regen',
        'regnen',
        'regnet',
        'sonne',
        'sonnig',
        'temperatur',
        'temperaturen',
        'kalt',
        'warm',
        'schnee',
        'schneit',
    ]

    # Liste mit allen möglichen Städten, für die das Wetter bestimmt werden kann.
    city_names = [
        "München",
        "Berlin",
        "Stuttgart",
        "Hamburg",
        "New York",
        "Los Angeles",
        "Chicago",
        "London",
    ]

    """
    message enthält die Eingabe der Benutzer*in.
    Durch die Funktion lower() wird jeder Buchstade der Eingabe der Benutzer*in klein geschrieben.
    Wenn zum Beispiel die Benutzer*in "Hallo wie geht es Ihnen" eintippt wird daraus "hallo wie geht es ihnen".
    Dieses Ergebnis wird dann der Variable message_lower zugewiesen.
    """
    message_lower = message.lower()

    # Variable mit der überprüft wird, ob die Benutzer*in eine Stadt in ihrer Anfrage angegeben hat, die in der Liste
    # city_names vorkommt
    city = None

    # Variable mit der überprüft wird, ob die Benutzer*in einen Wetterbegriff in ihrer Anfrage angegeben hat, die in
    # der Liste intents vorkommt
    intent = False

    # Für jede Stadt in der Liste city_names
    for possible_city in city_names:
        # Überprüfe, ob die Stadt in der Anfrage vorkommt
        if possible_city.lower() in message_lower:
            # Kommt die Stadt vor, setze die Variable city auf den Städtenamen
            city = possible_city
            # Durch den Befehl break wird die for Schleife abgebrochen
            break

    # Für jedes Wort in der Liste intents
    for possible_intent in intents:
        # Überprüfe, ob dieses Wort in der Anfrage vorkommt
        if possible_intent in message_lower:
            # Setze die Variable intent auf den Wert True (True=Wahr und False=Falsch)
            intent = True
            # Durch den Befehl break wird die for Schleife abgebrochen
            break

    # Die Funktion create_weather_response wird aufgerufen.
    # Der Funktion werden die Variablen city und intent übergeben.
    answer = create_weather_response(city, intent)

    # Gebe die Antwort zurück, die dann im Chat-Interface angezeigt wird
    return answer


def main():
    """
    Diese Funktion wird nach dem Start des Programms aufgerufen.
    Diese Funktion bekommt keine Parameter übergeben, da nichts in den Klammern angegeben ist.
    """

    # gr.Chatbot ist eine Klasse zur Erzeugung der Chat-Oberfläche.
    # Dokumentation: https://www.gradio.app/docs/chatbot
    chatbot = gr.Chatbot(
        value=[[None, "Ich bin der Wetter-Bot und beantworte dir Fragen zu dem Wetter in deiner Stadt"]],
        label="Wetter-Bot",
        show_label=True,
        container=True
    )

    # gr.ChatInterface ist eine Klasse die es ermöglicht, eine webbasierte Demo um das Chatbot-Modell zu erstellen.
    # Dokumentation: https://www.gradio.app/docs/chatinterface
    weather_chatbot = gr.ChatInterface(
        fn=response,
        chatbot=chatbot,
        retry_btn=None,
        undo_btn=None
    )

    # Startet einen einfachen Webserver, auf dem die Demo läuft.
    weather_chatbot.launch(inbrowser=True)


if __name__ == '__main__':
    # Wenn das Programm ausgeführt wird, startet man hier!
    # Als Erstes wird also die Funktion mit dem Namen main aufgerufen.
    main()
