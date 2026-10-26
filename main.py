import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)


    tipo = ft.TextField(label="Tipo")
    marca = ft.TextField(label="Marca")
    anno = ft.TextField(label="Anno acquisto")

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    valore = ft.TextField(width=100,
                          value="0",
                          border={
                              ft.ControlState.DEFAULT: ft.OutlineInputBorder(
                                  side=ft.BorderSide(color="grey", width=1)),
                              ft.ControlState.DISABLED: ft.OutlineInputBorder(
                                  side=ft.BorderSide(color="grey", width=1))
                          },
                          text_align=ft.TextAlign.CENTER)


    def decrementa_valore(e):
        val_attuale = float(valore.value)
        valore.value = str(val_attuale - 1)
        valore.update()

    def incrementa_valore(e):
        val_attuale = float(valore.value)
        valore.value = str(val_attuale + 1)
        valore.update()


    btnMinus = ft.IconButton(icon=ft.Icons.REMOVE,
                             icon_color="red",
                             icon_size=24, on_click=decrementa_valore)
    btnAdd = ft.IconButton(icon=ft.Icons.ADD,
                           icon_color="green",
                           icon_size=24, on_click=incrementa_valore)

    row1 = ft.Row([btnMinus, valore, btnAdd],
              alignment=ft.MainAxisAlignment.CENTER)


    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"


    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    def agg_strumento(e):
        # Controllo se i campi sono vuoti
        if not tipo.value or not marca.value or not anno.value:
            alert.show_alert("❌ Errore: compila tutti i campi: tipo, marca e anno")
            return  # Non aggiungo dati vuoti

        # Controllo se i valori inseriti sono del tipo corretto
        if not anno.value.isdigit():
            alert.show_alert("❌ Errore: inserisci un valore valido per l'anno")
            return # Non aggiungo dati non validi

        # Prima di chiamare la funzione per aggiungere il nuovo strumento converto anno e valore in numeri
        anno_convertito = int(anno.value)
        valore_convertito = float(valore.value)

        # Chiamo la funzione aggiungi_strumento passando i values
        deposito.aggiungi_strumento(tipo.value, marca.value, anno_convertito, valore_convertito)

        tipo.value = ""
        marca.value = ""
        anno.value = ""
        valore.value = "0"

        aggiorna_lista_strumenti()
        page.update()


    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    pulsante_aggiungi_strumento = ft.Button("Aggiungi strumento", on_click=agg_strumento)


    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        ft.Divider(),
        ft.Text(value=f"Inserisci nuovo strumento:", size=24, weight=ft.FontWeight.BOLD),
        ft.Row(spacing=50, controls=[tipo, marca, anno, row1], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(spacing=200,
               controls=[pulsante_aggiungi_strumento],
               alignment=ft.MainAxisAlignment.CENTER),


        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.run(main)
