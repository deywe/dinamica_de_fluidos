import py5
import pandas as pd
import numpy as np

# Configurações do Visualizador
LARGURA, ALTURA = 1280, 720
ARQUIVO_CSV = 'auditoria_fluidos_lyra_signed.csv'

def setup():
    py5.size(LARGURA, ALTURA, py5.P2D)
    py5.background(0)
    
    # Carregando o Dataset de Auditoria
    global df, total_frames
    try:
        print(f"📂 Abrindo dataset: {ARQUIVO_CSV}...")
        df = pd.read_csv(ARQUIVO_CSV)
        total_frames = df['frame'].max()
        print(f"✅ Sucesso: {len(df)} pontos de dados carregados.")
    except FileNotFoundError:
        print(f"❌ ERRO: O arquivo '{ARQUIVO_CSV}' não foi encontrado.")
        py5.exit_sketch()

def draw():
    # Efeito de rastro para visualizar as linhas de fluxo (streamlines)
    py5.fill(0, 0, 0, 15)
    py5.rect(0, 0, py5.width, py5.height)
    
    # Sincronização com o Frame do Dataset
    frame_atual = py5.frame_count % (total_frames + 1)
    
    # Filtragem dos dados (Seleciona apenas a fatia do frame atual)
    dados_frame = df[df['frame'] == frame_atual]
    
    # Renderização Ponto a Ponto
    for row in dados_frame.itertuples():
        # Mapeamento das coordenadas normalizadas (0-1) para a tela
        x_screen = row.x * py5.width
        y_screen = row.y * py5.height
        
        # A cor é extraída diretamente do valor de fase (phi) auditado
        # Isso garante que a cor reflita a física gravada, não uma estética
        p_val = np.clip((row.phi + 0.5), 0, 1)
        
        # Gradiente Ciano -> Magenta (Fase Quântica)
        py5.stroke(int(py5.lerp(0, 255, p_val)), 
                   int(py5.lerp(255, 100, p_val)), 
                   255, 180)
        
        py5.point(x_screen, y_screen)

    # HUD de Auditoria de Campo
    desenhar_hud(frame_atual)

def desenhar_hud(f):
    py5.no_stroke()
    py5.fill(0, 255, 255, 50)
    py5.rect(15, 15, 400, 80)
    
    py5.fill(255)
    py5.text_size(14)
    py5.text(f"MODO: AUDITORIA DE DATASET CSV", 25, 40)
    py5.fill(0, 255, 255)
    py5.text(f"FRAME ATUAL: {f:04d} / {total_frames}", 25, 60)
    py5.text(f"PONTOS POR FRAME: {len(df)//(total_frames+1)} particles", 25, 80)

def key_pressed():
    if py5.key == ' ': # Espaço para pausar a análise
        if py5.is_looping:
            py5.no_loop()
            print("⏸ Auditoria Pausada para inspeção de frame.")
        else:
            py5.loop()
            print("▶ Auditoria Retomada.")

py5.run_sketch()
