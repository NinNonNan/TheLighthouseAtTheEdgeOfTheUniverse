from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex
import requests
from datetime import datetime,time
from math import floor


class Card:
    def __init__(self, value, seed, color):
        self.value = value
        self.seed = seed
        self.color = color

    def __str__(self):
        return f"{self.value} di {self.seed}"

class IlFaroAlConfineDellUniverso(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.8, 0.9)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        # Window.size = (360, 640)
        # Nino BlackView
        # Window.size = (1080, 2340)
        Window.size = (540, 1170)
        Window.clearcolor = ('#323F61')

        self.window.add_widget(Image(
            source='background.png',
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1, 1)
        ))


        # Setacciare la spiaggia
        self.btn_s = Button(
            text="Setacciando la spiaggia",
            size_hint=(1, 0.15),
            bold=True,
            italic=True,
            background_color='#323F61'
        )
        # La spiaggia si setaccia la mattina.
        # Dalle 5:00 alle 12:00
        if datetime.now().time() <= time(19, 0) and datetime.now().time() >= time(5,0):
            self.window.add_widget(self.btn_s)
            self.btn_s.bind(on_press=self.search)


        # Accendere la luce
        self.btn_t = Button(
            text="Accendere la luce",
            size_hint=(1, 0.15),
            bold=True,
            italic=True,
            background_color='#323F61'
        )
        # La luce del faro va accesa dall'alba al tramonto.
        # Dalle 19:00 alle 5:00
        # TODO Sarebbe bello calcolare alba e tramonto via API ;)
        if datetime.now().time() <= time(5, 0) or datetime.now().time() >= time(18,0):
            self.window.add_widget(self.btn_t)
            self.btn_t.bind(on_press=self.turn_light)

        # Manutenzione
        self.btn_m = Button(
            text="Manutenzione",
            size_hint=(1, 0.15),
            bold=True,
            italic=True,
            background_color='#323F61'
        )
        self.window.add_widget(self.btn_m)
        self.btn_m.bind(on_press=self.maintenance)

        # Osservazione
        self.btn_w = Button(
            text="Osservazione",
            size_hint=(1, 0.15),
            bold=True,
            italic=True,
            background_color='#323F61'
        )
        self.window.add_widget(self.btn_w)
        self.btn_w.bind(on_press=self.watch)

        # Evento
        self.btn_e = Button(
            text="Evento",
            size_hint=(1, 0.15),
            bold=True,
            italic=True,
            background_color='#323F61'
        )
        self.window.add_widget(self.btn_e)
        self.btn_e.bind(on_press=self.event)
 
        self.lblMain = Label(
            text="...",
            size_hint=(0.8, 0.2),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            font_size='20sp',
            padding=(10, 0, 10, 0),
            italic=True
        )
        self.window.add_widget(self.lblMain)

        self.lblSub = Label(
            text="...",
            size_hint=(0.8, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            font_size='14sp',
            padding=(10, 0, 10, 0),
            italic=True
        )
        self.window.add_widget(self.lblSub)


        self.tentativi_necessari = 0
        return self.window

    def turn_light(self, instance):
        self.tentativi_necessari = 0
        while True:
            self.tentativi_necessari += 1
            card = self.draw_card()
            coin = self.flip_coin()

            if card.color == 'RED' and coin:
                break

        if self.tentativi_necessari == 1:
            self.lblMain.text = f"Hai acceso la luce al primo tentativo."
        else:
            self.lblMain.text = f"Hai acceso la luce in {self.tentativi_necessari} tentativi."
        
        self.btn_t.text = "La luce ora è accesa"
        self.btn_t.color = '#FFFF00'

    def search(self, instance):
        #current_time = datetime.now().time()
        self.foundItem = floor(datetime.now().time().hour / 2)      
        self.lblMain.text = f"Hai trovato {self.foundItem} oggetti."

    def maintenance(self, instance):
        dice = self.roll_dice(15)
        card = self.draw_card()

        # Definisci un array di eventi in base al tiro del dado
        events = {
            1: 'è fratturato',
            2: 'è frantumato',
            3: 'è incrinato',
            4: 'si è slacciato',
            5: 'si è disfatto',
            6: 'ha bisogno di cure',
            7: 'ha bisogno di attenzioni',
            8: "manca",
            9: "è andata persa",
            10: "è smarrita",
            11: 'è scricchiolante',
            12: 'è traballante',
            13: 'è cigolante',
            14: "ha bisogno di ordine",
            15: "ha bisogno di essere sistemato"
        }

        # Definisci un array di descrizioni in base al seme della carta
        descriptions = {
            '♠': "Un imprevisto accade mentre stai completando l'attività.",
            '♣': "Le cose non si mettono a tuo favore.",
            '♥': "Durante il compito, ti assale un ricordo evocativo.",
            '♦': "Tutto procede secondo i tuoi piani."
        }

        event = events.get(dice, f"Evento sconosciuto con valore numerico {dice}")
        description = descriptions.get(card.seed, "Descrizione sconosciuta per il seme della carta.")

        self.lblMain.text = f"Qualcosa {event}"
        self.lblSub.text = f"{description}"

    def watch(self, instance):
        dice = self.roll_dice(6)
        card = self.draw_card()

        # Definisci un array di eventi in base al tiro del dado
        events = {
            1: 'Animali',
            2: 'Navi spaziali',
            3: 'Qualcosa nel cielo',
            4: 'Strutture',
            5: 'Alieni',
            6: 'Esseri'
        }

        # Definisci un array di descrizioni in base al seme della carta
        descriptions = {
            '♠': "Puntino lontano, lampo di luce.",
            '♣': "Oltre il raggio del faro, distanza sicura.",
            '♥': "A un braccio di distanza dall’isola.",
            '♦': "Sopra la tua testa."
        }

        event = events.get(dice, f"Evento sconosciuto con valore numerico {dice}")
        description = descriptions.get(card.seed, "Descrizione sconosciuta per il seme della carta.")

        self.lblMain.text = f"Vedi {event}"
        self.lblSub.text = f"{description}"

    def event(self, instance):
        card = self.draw_card()

        events = {
            '2': 'Una collisione',
            '3': 'Un blackout totale',
            '4': 'La luce del faro si spegne',
            '5': "All'improvviso tutto diventa silenzioso",
            '6': 'Ricevi un messaggio dai tuoi cari',
            '7': "Ricevi un segnale misterioso dall'universo",
            '8': 'La gravità smette di funzionare',
            '9': 'Il tempo si distorce in avanti',
            '10': 'Vedi una nave in difficoltà',
            'J': 'Ti rendi conto di non essere solo',
            'Q': "Senti un'esplosione",
            'K': "Il tempo si distorce all'indietro",
            'A': "Un viaggiatore visita il faro"
        }

        consequences = {
            'RED': 'durature',
            'BLACK': 'passeggere'
        }

        event = events.get(card.value, f"Evento {card.value}")
        consequence = consequences.get(card.color, f"Colore {card.color}")

        self.lblMain.text = f"{event}"
        self.lblMain.italic = True
        self.lblSub.text = f"Conseguenze {consequence}"

    def draw_card(self):
        api_url = "https://www.random.org/integers/"
        params = {
            "num": 1,
            "min": 1,
            "max": 13,
            "col": 1,
            "base": 10,
            "format": "plain",
            "rnd": "new"
        }

        response = requests.get(api_url, params=params)
        value = int(response.text.strip())

        params["num"] = 1
        params["min"] = 1
        params["max"] = 4

        response = requests.get(api_url, params=params)
        seed = int(response.text.strip())

        seeds = {1: '♣', 2: '♦', 3: '♥', 4: '♠'}
        values = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}
        colors = {1: 'BLACK', 2: 'RED'}

        seed = seeds.get(seed, str(seed))
        value = values.get(value, str(value))
        color = colors[1] if seed in ['♥', '♦'] else colors[2]

        card_generated = Card(value, seed, color)
        return card_generated

    def flip_coin(self):
        api_url = "https://www.random.org/integers/"
        params = {
            "num": 1,
            "min": 0,
            "max": 1,
            "col": 1,
            "base": 10,
            "format": "plain",
            "rnd": "new"
        }

        response = requests.get(api_url, params=params)
        risultato_moneta = int(response.text.strip())

        return risultato_moneta == 0

    def roll_dice(self, max_value):
        api_url = "https://www.random.org/integers/"
        params = {
            "num": 1,
            "min": 1,
            "max": max_value,
            "col": 1,
            "base": 10,
            "format": "plain",
            "rnd": "new"
        }

        response = requests.get(api_url, params=params)
        dice_result = int(response.text.strip())

        return dice_result

IlFaroAlConfineDellUniverso().run()
