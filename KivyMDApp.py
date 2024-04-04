from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.core.window import Window
from kivy.uix.image import Image
import requests
from datetime import datetime, time
from math import floor

class Card:
    def __init__(self, value, seed, color):
        self.value = value
        self.seed = seed
        self.color = color

    def __str__(self):
        return f"{self.value} di {self.seed}"

class IlFaroAlConfineDellUniverso(MDApp):
    def build(self):
        self.window = MDBoxLayout(
            orientation='vertical',
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        Window.size = (int(540 * 0.8), int(1170 * 0.8))
        self.window.md_bg_color = ('#323F61')

        self.window.add_widget(Image(
            source='background.png',
            size_hint=(1, 1)
        ))

        # Definisci attributi di stile per i BoxLayout
        bl_style = {
            "orientation": 'vertical',
            "size_hint": (0.8, 0.3),
            "spacing": 8
        }

        btn_layout = MDBoxLayout(
            pos_hint={'center_x': 0.5},
            **bl_style
        )      
        self.window.add_widget(btn_layout)

        lbl_layout = MDBoxLayout(
            pos_hint={'center_x': 0.5},
            **bl_style
        )      
        self.window.add_widget(lbl_layout)

        # Definisci attributi di stile per i bottoni
        btn_style = {
            "theme_text_color": "Custom",
            "text_color": '#F8FBFB',
            "md_bg_color": '#526286',
            "size_hint": (0.9, 0.2),
            "pos_hint": {'center_x': 0.5},
            "font_name":"font/ADKLRR-IM_FELL_Great_Primer_SC.ttf"
        }
        
        # Definisci attributi di stile per le label
        lbl_style = {
            "theme_text_color": "Custom",
            "italic":True,
            "halign":"center",
            "text_color":'#F8FBFB'
        }

        self.btn_s = MDFlatButton(
            text='SETACCIARE LA SPIAGGIA',
            on_press=self.search,
            **btn_style
        )

        # Definisco l'ora corrente
        now = datetime.now().time()
        
        if now <= time(20, 0) and now >= time(5,0):
            btn_layout.add_widget(self.btn_s)

        self.btn_t = MDFlatButton(
            text='ACCENDERE LA LUCE',
            on_press=self.toggle_light,
            **btn_style
        )
        if now <= time(5, 0) or now >= time(12,0):
            btn_layout.add_widget(self.btn_t)

        # Aggiungi un attributo di stato al bottone
        self.btn_t.light_on = False

        self.btn_m = MDFlatButton(
            text='MANUTENZIONE',
            on_press=self.maintenance,
            **btn_style
        )
        btn_layout.add_widget(self.btn_m)

        self.btn_w = MDFlatButton(
            text='OSSERVAZIONE',
            on_press=self.watch,
            **btn_style
        )
        btn_layout.add_widget(self.btn_w)

        self.btn_e = MDFlatButton(
            text='EVENTO',
            on_press=self.event,
            **btn_style
        )
        btn_layout.add_widget(self.btn_e)

        self.lblMain = MDLabel(
            text="...",
            **lbl_style
        )
        lbl_layout.add_widget(self.lblMain)

        self.lblSub = MDLabel(
            text="...",
            **lbl_style
        )
        lbl_layout.add_widget(self.lblSub)

        return self.window

    def toggle_light(self, instance):
        if not self.btn_t.light_on:
            self.turn_light(instance)
        else:
            self.off_light(instance)
    
    def turn_light(self, instance):
        self.attempts_needed = 0
        success = False

        while not success and self.attempts_needed < 10:
            self.attempts_needed += 1
            card = self.draw_card()
            coin = self.flip_coin()

            if card.color == 'RED' and coin:
                success = True

        if success:
            if self.attempts_needed == 1:
                self.lblMain.text = "Hai acceso la luce del faro."
            else:
                self.lblMain.text = f"Hai acceso la luce dopo molti tentativi."

            self.btn_t.text = 'SPEGNERE LA LUCE'
            self.btn_t.text_color = '#FFFF00'
            self.btn_t.light_on = True
        else:
            self.lblMain.text = "Non riesci ad accendere la luce."
            
    def off_light(self, instance):
        self.lblMain.text = "Hai spento la luce del faro."
        self.btn_t.text = 'ACCENDERE LA LUCE'
        self.btn_t.text_color = '#F8FBFB'
        self.btn_t.light_on = False

    def search(self, instance):
        self.foundItem = floor(datetime.now().time().hour / 2)      
        self.lblMain.text = f"Hai trovato {self.foundItem} oggetti."

        card = self.draw_card()

        # Il primo elemento è la categoria generale, i successivi sono i dettagli
        items = {
            '2': ['Corpi','scheletri', 'arti', 'denti', 'pelliccia', 'squame', 'corna', 'interiora'],
            '3': ['Animali','uccelli', 'pesci', 'rettili', 'razze galattiche', 'balene spaziali'],
            '4': ['Detriti di astronavi','pannelli', 'portelli', 'motori', 'condutture', 'tubi', 'mobili', 'schermi', 'ali'],
            '5': ['Viaggiatore','umano', 'alieno', 'robot', 'essere sconosciuto', 'creatura'],
            '6': ['Tecnologia','cavi', 'chip', 'schede', 'antenne', 'dischi rigidi'],
            '7': ['Dispositivi','cacciaviti', 'orologi', 'telescopi', 'dispositivi di registrazione', 'termometri', 'comunicatori'],
            '8': ['Messaggio','in una bottiglia', 'in uno scrigno', 'in un barattolo', 'su carta', 'su un chip'],
            '9': ['Flora','legno', 'rampicanti', 'semi', 'radici', 'fiori'],
            '10': ['Rocce spaziali','meteore', 'pietre preziose', 'rocce luminose', 'pezzi di stelle'],
            'J': ['Armi','laser', 'lame', 'esplosivi', 'veleno'],
            'Q': ['Tessuto','vestiti', 'tute spaziali', 'stracci', 'vele', 'scampoli', 'reti', 'borse'],
            'K': ['Documento','diari', 'libri', 'dischi dati', 'lettere', 'chiavette USB', 'mappe'],
            'A': ['Ricchezze','gioielli', 'monete', 'carte di credito', 'pietre preziose', 'banconote']
        }
        # Usa roll_dice per ottenere un risultato casuale
        item = items.get(card.value, [])[0]
        dice_result = self.roll_dice(len(items.get(card.value, []))-1)
        item_detail = items.get(card.value, [])[dice_result]

        self.lblMain.text = f"Hai trovato {item}."
        self.lblSub.text = f"Hai trovato {item_detail}."

    def maintenance(self, instance):
        dice = self.roll_dice(15)
        card = self.draw_card()

        events = {
            1: 'è fratturato',
            2: 'è frantumato',
            3: 'è incrinato',
            4: 'si è slacciato',
            5: 'si è disfatto',
            6: 'ha bisogno di cure',
            7: 'ha bisogno di attenzioni',
            8: 'manca',
            9: 'è andata persa',
            10: 'è smarrita',
            11: 'è scricchiolante',
            12: 'è traballante',
            13: 'è cigolante',
            14: 'ha bisogno di ordine',
            15: 'ha bisogno di essere sistemato'
        }

        descriptions = {
            '♠': "Un imprevisto accade mentre stai completando l'attività.",
            '♣': 'Le cose non si mettono a tuo favore.',
            '♥': 'Durante il compito, ti assale un ricordo evocativo.',
            '♦': 'Tutto procede secondo i tuoi piani.'
        }

        event = events.get(dice, f"Evento sconosciuto con valore numerico {dice}")
        description = descriptions.get(card.seed, "Descrizione sconosciuta per il seme della carta.")

        self.lblMain.text = f"Qualcosa {event}"
        self.lblSub.text = f"{description}"

    def watch(self, instance):
        dice = self.roll_dice(6)
        card = self.draw_card()

        events = {
            1: 'Animali',
            2: 'Navi spaziali',
            3: 'Qualcosa nel cielo',
            4: 'Strutture',
            5: 'Alieni',
            6: 'Esseri'
        }

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
