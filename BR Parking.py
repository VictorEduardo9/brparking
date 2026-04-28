import PySimpleGUI as sg
import time
import ctypes

bg = '#fff5e2'
topbar_color='#491d00'
sg.theme('Reddit')
sg.set_options(background_color='#fff5e2')

motos = 0
carros = 0
dados = []
maximizado=True

# Animações
def fadein(window, step=0.05, delay=50):
    for i in range (0,21):
        window.set_alpha(i*step)
        window.refresh()
        time.sleep(delay/1000)

def fadeout(window, step=0.05, delay=10):
    for i in range (20,-1,-1):
        window.set_alpha(i*step)
        window.refresh()
        time.sleep(delay/1000)

# Barra
def barratitulo(titulo):
    return [
        sg.Column(
            [[sg.Text('BR Parking', text_color='white' , background_color=topbar_color, font=('SF Pro Display', 14, 'bold'), pad=(10,5)),
            sg.Push(),
            sg.Text('—', key='minimizar',
            enable_events=True, text_color='white' ,
            background_color=topbar_color,
            font=('SF Pro Display', 14),
            pad=(10,5)),

            sg.Text('🗗', key='restaurar',
            enable_events=True, text_color='white',
            background_color=topbar_color,
            font=('SF Pro Display', 14),
            pad=(10, 5)),

            sg.Text('❌',
            key='fechar',
            enable_events=True,
            text_color='white',
            background_color=topbar_color,
            font=('SF Pro Display', 14),
            pad=(10,5))

        ]],
        background_color=topbar_color,
        expand_x=True,
        grab=True
        )
    ]

# Botões grandes
def botao(texto):
    return sg.Button(
        texto,
        font=('SF Pro Display', 16,),
        button_color=('white' , '#491d00'),
        border_width=0,
        expand_x=True,
        expand_y=True,
        pad=(15,12),
        mouseover_colors=('white', '#2e0200')
    )

# PopUps

def popups(mensagem):
    layout=[
        [sg.Text(mensagem, font=('SF Pro Display', 18), text_color='black' , background_color=bg, justification='center')],
        [sg.Text('', size=(1, 1), background_color=bg)],
        [sg.Push(background_color=bg),
        sg.Button('Ok', size=(10,1), button_color=('white' , '#491d00'), border_width=0, font=('SF Pro Display', 14)),
        sg.Push(background_color=bg)]
    ]

    janelapopup = sg.Window(
        '', layout,  modal=True, finalize=True , background_color=bg , no_titlebar=True , alpha_channel=0)

    janelapopup.refresh()
    time.sleep(0.05)
    fadein(janelapopup)
    while True:
        eventos, valores = janelapopup.read()
        if eventos == 'Ok':
            break
    fadeout(janelapopup)
    janelapopup.close()

# Selecionar horario
def selecionarhorario():
    layout = [
        [sg.Text('Selecione o horário de entrada', font=('SF Pro Display', 24) , background_color=bg)],

        [sg.Text('Hora:', font=('SF Pro Display' , 14) , background_color=bg),
        sg.Spin([f"{i:02d}" for i in range (12 , 23)], initial_value='12', key='hora' , size=(8,2) , readonly=True),

        sg.Text('Minuto:', font=('SF Pro Display' , 14) , background_color=bg),
        sg.Spin([f"{i:02d}" for i in range(60)], initial_value='00', key='minuto' , size=(8,2) , readonly=True)],

        [sg.Button('Confirmar', font=('SF Pro Display' , 13) , button_color=('white', '#491d00')),
        sg.Button('Cancelar', font=('SF Pro Display' , 13) , button_color=('white', '#491d00'))]
    ]
    janela = sg.Window('', layout, modal=True, finalize=True , background_color=bg , no_titlebar=True , alpha_channel=0)
    fadein(janela)

    while True:
        eventos, valores = janela.read()
        if eventos == 'Confirmar':
            hora = int(valores['hora'])
            minuto = int(valores['minuto'])
            horario = f"{hora:02d}:{minuto:02d}"
            fadeout(janela)
            janela.close()
            return horario

        if eventos == 'Cancelar':
            fadeout(janela)
            janela.close()
            return None

# Relatorio
def mostrarrelatorio(carros, motos):
    barratitulo('Relatório'),
    texto = '\n'.join([f"{d['tipoveiculo'].capitalize()}  -  {d['horario']}" for d in dados]) or 'Sem registros'
    layoutrelatorio = [
        [sg.Text('Relatório', font=('SF Pro Display' , 22 , 'bold'), background_color=bg)],
        [sg.Text(texto, font=('SF Pro Display' , 14 ) , background_color=bg)],

        [sg.Button('Ok', size=(10,2) , button_color='#491d00' , font=('SF Pro Display', 22))]

    ]

    janelarelatorio = sg.Window('', layoutrelatorio, modal=True, finalize=True, element_justification='center' , alpha_channel=0, no_titlebar=True)
    janela.refresh()
    time.sleep(0.05)

    fadein(janelarelatorio)

    while True:
        eventos, valores = janelarelatorio.read()
        if eventos == 'fechar':
            break
        if eventos == 'Ok':
            break

    fadeout(janelarelatorio)
    janelarelatorio.close()

# Menu de escolher veiculos
def escolherveiculo():
    layoutveiculo = [
        [sg.Text('Selecione o tipo de veículo desejado', font=('SF Pro Display', 24, 'bold'), text_color='black' , background_color='#fff5e2')],
        [sg.Push(background_color=bg), sg.Button('Carro', size=(15,2) , font=('SF Pro Display' , 13) , button_color='#491d00' ,  border_width=2, mouseover_colors=('white','#491d00')),

        sg.Button('Moto', size=(15,2) , font=('SF Pro Display' , 13) , button_color='#491d00' , border_width=2, mouseover_colors=('white','#491d00')) ,

        sg.Button('Cancelar', size=(15,2) , font=('SF Pro Display' , 13) , button_color='#491d00' , border_width=2, mouseover_colors=('white','#491d00')) , sg.Push(background_color=bg)]
    ]

    janela = sg.Window('Selecionar veículo' , layoutveiculo, background_color='#fff5e2' , modal=True, finalize=True, alpha_channel=0 , no_titlebar=True)
    janela.refresh()
    time.sleep(0.05)
    fadein(janela)

    while True:
        eventos, valores = janela.read()
        if eventos == 'fechar':
            return None
        if eventos == 'Cancelar':
            fadeout(janela)
            janela.close()
            return 'cancelar'
        if eventos == 'Carro':
            fadeout(janela)
            janela.close()
            return 'carro'
        if eventos == 'Moto':
            fadeout(janela)
            janela.close()
            return 'moto'
# Layout Botoes
layoutbotoes = [
    [botao('Registrar  Veículo')],
    [sg.Text('', size=(1,1) , background_color='#fff5e2')],
    [botao('Relatório')],
    [sg.Text('', size=(1,1) , background_color='#fff5e2')],
    [botao('Sair')]
]
# Layout
layout = [
    barratitulo('BR Parking'),
    [sg.Push(background_color=bg), sg.Text('Estacionamento BR Parking', font=('SF Pro Display', 74, 'bold'), background_color=bg ,text_color='black') ,sg.Push(background_color=bg)],
[   sg.Push(background_color=bg), sg.Text('Bem-vindo ao Estacionamento BR Parking', font=('SF Pro Display', 37), background_color=bg , text_color='black') , sg.Push(background_color=bg)],

    [sg.Text('', size=(1,4), background_color=bg)],

    [
        sg.Push(background_color=bg),
        sg.Frame('', layoutbotoes, size= (920,530), pad=(30,30), border_width=0,
        background_color=bg , relief=sg.RELIEF_FLAT , expand_x=True, expand_y=True),
        sg.Push(background_color=bg)
    ],

    [sg.VPush(background_color=bg)]
]
# Janela
janela = sg.Window('BR Parking', layout , resizable=True , finalize=True, alpha_channel=0 , background_color=bg , no_titlebar = True )
janela.refresh()
time.sleep(0.05)
janela.maximize()
fadein(janela)

user32 = ctypes.WinDLL('user32')
hwnd = ctypes.windll.user32.GetAncestor(janela.TKroot.winfo_id(), 2)
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080
style=user32.GetWindowLongW(hwnd, -20)
style=(style & ~WS_EX_TOOLWINDOW) | WS_EX_APPWINDOW
user32.SetWindowLongW(hwnd, -20, style)



# Ler os eventos
while True:
    eventos, valores = janela.read()

    if eventos == sg.WIN_CLOSED:
        break
    if eventos == 'minimizar':
        user32 = ctypes.WinDLL('user32')
        hwnd = ctypes.windll.user32.GetAncestor(janela.TKroot.winfo_id(), 2)
        user32.ShowWindow(hwnd, 6)
    if eventos == 'restaurar':
        if maximizado:
            janela.normal()
            maximizado = False
        else:
            janela.maximize()
            maximizado = True
    if eventos == 'fechar':
        break
    if eventos == 'Sair':
        break
    if eventos == 'Registrar  Veículo':
        tipoveiculo = escolherveiculo()
        if tipoveiculo in ('carro , moto'):
            horario = selecionarhorario()
            if horario:
                dados.append({
                    'tipoveiculo': tipoveiculo,
                    'horario': horario
                })
                if tipoveiculo == 'carro':
                    carros += 1
                    popups('Veiculo registrado com sucesso')
                elif tipoveiculo == 'moto':
                        motos += 1
                        popups('Veiculo registrado com sucesso')
        elif tipoveiculo == 'cancelar':
            popups('Retornando ao ínicio do menu')
        else:
            popups('Tipo inválido')


    if eventos == 'Relatório':
        mostrarrelatorio(carros, motos)


fadeout(janela)
janela.close()