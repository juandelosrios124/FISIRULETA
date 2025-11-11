import pygame
import sys
import json
import random
import copy
import os # Para construir rutas de archivos

# --- 1. Inicialización de Pygame ---
pygame.init()

# --- 2. Constantes y Configuración ---

# Dimensiones de la pantalla
ANCHO_PANTALLA = 1200
ALTO_PANTALLA = 600

# --- 2. Colores ---
# (Tus colores existentes)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS_CLARO = (200, 200, 200)
GRIS_OSCURO = (100, 100, 100)
AZUL_TITULO = (50, 150, 255)
VERDE_CORRECTO = (76, 175, 80)
ROJO_INCORRECTO = (244, 67, 54)
COLOR_BOTON_NORMAL = (100, 100, 255) # Azul suave
COLOR_BOTON_HOVER = (150, 150, 255) # Azul más claro para hover

# NUEVO COLOR
COLOR_TITULO_VICTORIA = (255, 223, 0) # Un dorado brillante para la victoria

# Colores para las categorías de la ruleta
COLOR_CATEGORIAS = {
    "Campo Electrico": (231, 76, 60), # Rojo
    "Corriente": (52, 152, 219),      # Azul
    "Temperatura": (241, 196, 15),     # Amarillo
    "DEFAULT": (127, 140, 141)
}

# Nombres de los personajes (basados en categorías)
LISTA_PERSONAJES = ["Campo Electrico", "Corriente", "Temperatura"]

# Fotogramas por segundo
FPS = 60

# Configuración de la pantalla
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Mi Juego de Preguntas")

# Reloj (para controlar los FPS)
clock = pygame.time.Clock()

# Ruta a la carpeta de imágenes
RUTA_IMAGENES = "imagenes"

# --- 3. Fuentes ---

# Definimos el nombre de tu archivo de fuente
NOMBRE_FUENTE = "Pixeltype.ttf"

try:
    # Intentamos cargar tu fuente personalizada.
    # ¡OJO! Las fuentes "pixel" a veces necesitan tamaños más grandes.
    # Es posible que tengas que experimentar con estos números.
    fuente_titulo = pygame.font.Font(NOMBRE_FUENTE, 70)
    fuente_pregunta = pygame.font.Font(NOMBRE_FUENTE, 25)
    fuente_opcion = pygame.font.Font(NOMBRE_FUENTE, 32)
    fuente_hud = pygame.font.Font(NOMBRE_FUENTE, 20)
    print(f"Fuente personalizada '{NOMBRE_FUENTE}' cargada exitosamente.")
    
except IOError:
    # Plan B: Si no se encuentra 'Pixeltype.ttf', usa la fuente por defecto.
    print(f"Error al cargar la fuente '{NOMBRE_FUENTE}'. Usando fuente por defecto de Pygame.")
    fuente_titulo = pygame.font.Font(None, 74)
    fuente_pregunta = pygame.font.Font(None, 48)
    fuente_opcion = pygame.font.Font(None, 36)
    fuente_hud = pygame.font.Font(None, 30)


# --- 3.5. Cargar Recursos (Imágenes) ---

def cargar_iconos():
    """
    MODIFICADO: Carga iconos, ruleta Y ahora también el fondo de la ruleta.
    """
    iconos_grandes = {}
    iconos_hud = {}
    
    TAMANO_ICONO_GRANDE = (100, 100)
    TAMANO_ICONO_HUD = (48, 48)
    
    overlay_desactivado = pygame.Surface(TAMANO_ICONO_HUD, pygame.SRCALPHA)
    overlay_desactivado.fill((0, 0, 0, 180)) 

    for pj in LISTA_PERSONAJES:
        nombre_archivo = f"{pj.lower().replace(' ', '_')}.png"
        ruta_completa = os.path.join(RUTA_IMAGENES, nombre_archivo)
        
        try:
            img = pygame.image.load(ruta_completa).convert_alpha()
            iconos_grandes[pj] = pygame.transform.scale(img, TAMANO_ICONO_GRANDE)
            iconos_hud[pj] = pygame.transform.scale(img, TAMANO_ICONO_HUD)
            
        except pygame.error as e:
            print(f"Error al cargar la imagen '{ruta_completa}': {e}")
            # ... (código de reemplazo) ...
            color = COLOR_CATEGORIAS.get(pj, "DEFAULT")
            img_grande = pygame.Surface(TAMANO_ICONO_GRANDE)
            img_grande.fill(color)
            iconos_grandes[pj] = img_grande
            img_hud = pygame.Surface(TAMANO_ICONO_HUD)
            img_hud.fill(color)
            iconos_hud[pj] = img_hud

    ruleta_imagen_base = None
    ruta_ruleta = os.path.join(RUTA_IMAGENES, "Rula.png")
    try:
        ruleta_imagen_base = pygame.image.load(ruta_ruleta).convert_alpha()
        img_rect = ruleta_imagen_base.get_rect()
        nuevo_ancho = 400
        escala = nuevo_ancho / img_rect.width
        nuevo_alto = int(img_rect.height * escala)
        ruleta_imagen_base = pygame.transform.scale(ruleta_imagen_base, (nuevo_ancho, nuevo_alto)) 
        print(f"Ruleta cargada y escalada a ({nuevo_ancho}, {nuevo_alto})")
    except pygame.error as e:
        print(f"Error al cargar la imagen de la ruleta '{ruta_ruleta}': {e}")
        print("La ruleta no se mostrará.")
    
    fondo_juego = None
    ruta_fondo_juego = os.path.join(RUTA_IMAGENES, "Fondo.jpg") 
    try:
        fondo_juego = pygame.image.load(ruta_fondo_juego).convert()
        fondo_juego = pygame.transform.scale(fondo_juego, (ANCHO_PANTALLA, ALTO_PANTALLA))
        print(f"Fondo de juego '{ruta_fondo_juego}' cargado y escalado.")
    except pygame.error as e:
        print(f"Error al cargar el fondo de juego '{ruta_fondo_juego}': {e}")

    fondo_victoria = None
    ruta_fondo_victoria = os.path.join(RUTA_IMAGENES, "Victoria.jpg") 
    try:
        fondo_victoria = pygame.image.load(ruta_fondo_victoria).convert()
        fondo_victoria = pygame.transform.scale(fondo_victoria, (ANCHO_PANTALLA, ALTO_PANTALLA))
        print(f"Fondo de victoria '{ruta_fondo_victoria}' cargado y escalado.")
    except pygame.error as e:
        print(f"Error al cargar el fondo de victoria '{ruta_fondo_victoria}': {e}")

    # --- NUEVO: Cargar el fondo de la ruleta ---
    fondo_ruleta = None
    ruta_fondo_ruleta = os.path.join(RUTA_IMAGENES, "fondo_ruleta.jpg") 
    try:
        fondo_ruleta = pygame.image.load(ruta_fondo_ruleta).convert()
        fondo_ruleta = pygame.transform.scale(fondo_ruleta, (ANCHO_PANTALLA, ALTO_PANTALLA))
        print(f"Fondo de ruleta '{ruta_fondo_ruleta}' cargado y escalado.")
    except pygame.error as e:
        print(f"Error al cargar el fondo de ruleta '{ruta_fondo_ruleta}': {e}")

    # MODIFICADO: Devolver también el fondo_ruleta
    return iconos_grandes, iconos_hud, overlay_desactivado, ruleta_imagen_base, fondo_juego, fondo_victoria, fondo_ruleta


# --- 4. Cargar y Organizar Datos ---

def cargar_preguntas(archivo_json):
    """
    Carga las preguntas desde un archivo JSON.
    Maneja errores si el archivo no se encuentra o tiene mal formato.
    """
    try:
        with open(archivo_json, 'r', encoding='utf-8') as f:
            preguntas = json.load(f)
        if not preguntas:
            print(f"Error: El archivo '{archivo_json}' está vacío.")
            return []
        print(f"Se cargaron {len(preguntas)} preguntas exitosamente.")
        return preguntas
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo_json}'.")
        print("Asegúrate de crear el archivo 'preguntas.json' en la misma carpeta.")
        return []
    except json.JSONDecodeError:
        print(f"Error: El archivo '{archivo_json}' tiene un formato JSON inválido.")
        return []
    except Exception as e:
        print(f"Ocurrió un error inesperado al cargar las preguntas: {e}")
        return []

def organizar_preguntas_por_categoria(lista_preguntas):
    """
    Organiza la lista de preguntas en un diccionario
    donde las claves son las categorías.
    """
    dict_preguntas = {}
    for pregunta in lista_preguntas:
        categoria = pregunta["categoria"]
        if categoria not in dict_preguntas:
            dict_preguntas[categoria] = []
        dict_preguntas[categoria].append(pregunta)
        
    # Barajamos las preguntas dentro de cada categoría
    for categoria in dict_preguntas:
        random.shuffle(dict_preguntas[categoria])
        
    print(f"Preguntas organizadas en {len(dict_preguntas)} categorías.")
    return dict_preguntas

def cargar_preguntas_finales(archivo_json):
    """
    NUEVO: Carga las 3 preguntas 'finales' o 'de personaje' desde un JSON.
    """
    try:
        with open(archivo_json, 'r', encoding='utf-8') as f:
            preguntas_finales = json.load(f)
        print(f"Se cargaron {len(preguntas_finales)} preguntas finales exitosamente.")
        return preguntas_finales
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo_json}'.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: El archivo '{archivo_json}' tiene un formato JSON inválido.")
        return {}

# --- 5. Funciones Auxiliares (Código Limpio) ---

def dibujar_texto(texto, fuente, color, superficie, x, y, centrado=False):
    """
    Función auxiliar para renderizar y dibujar texto en la pantalla.
    """
    obj_texto = fuente.render(texto, True, color)
    rect_texto = obj_texto.get_rect()
    
    if centrado:
        rect_texto.center = (x, y)
    else:
        rect_texto.topleft = (x, y)
        
    superficie.blit(obj_texto, rect_texto)
    return rect_texto # Devolvemos el rectángulo para detección de clics

def dibujar_hud(superficie, hud_data, iconos_hud, overlay):
    """
    NUEVO (Versión 2): Dibuja el HUD (Puntuación, Racha, Personajes).
    Puntos/Racha a la izquierda, Iconos de Personajes (solos) a la derecha.
    """
    puntuacion = hud_data['puntuacion']
    racha = hud_data['racha']
    personajes_obtenidos = hud_data['personajes']

    # HUD más alto (60px) para acomodar los nuevos iconos de 48x48
    hud_rect = pygame.Rect(0, 0, ANCHO_PANTALLA, 60)
    pygame.draw.rect(superficie, GRIS_CLARO, hud_rect)
    
    # Texto centrado verticalmente (aprox)
    y_texto_hud = 18 
    
    # --- Lado Izquierdo: Puntos y Racha ---
    dibujar_texto(f"Puntos: {puntuacion}", fuente_hud, NEGRO, superficie, 15, y_texto_hud)
    dibujar_texto(f"Racha: {racha}", fuente_hud, NEGRO, superficie, 180, y_texto_hud)
    
    # --- Lado Derecho: Iconos de Personajes (Quesitos) ---
    pos_x_icono = ANCHO_PANTALLA - 10 # Empezar desde el borde derecho con 10px padding
    y_icono = 6 # (60px HUD - 48px Icono) / 2
    
    # Iteramos en REVERSA para colocarlos de derecha a izquierda
    for personaje in reversed(LISTA_PERSONAJES): 
        
        # Mover la posición X para el *inicio* de este icono
        pos_x_icono -= 48 # Ancho del icono (48x48)
        
        if personaje in iconos_hud:
            icono = iconos_hud[personaje]
            superficie.blit(icono, (pos_x_icono, y_icono))
            
            # Overlay si no está obtenido
            if not personajes_obtenidos.get(personaje, False):
                superficie.blit(overlay, (pos_x_icono, y_icono))
        
        # Mover la posición X para el *siguiente* icono (con padding)
        pos_x_icono -= 15 # Padding de 15px entre iconos


# --- 6. Pantallas (Máquina de Estados) ---

def pantalla_inicio(fondo_juego):
    """
    MODIFICADO: Acepta y dibuja el fondo_juego.
    """
    ancho_boton = 250
    alto_boton = 70
    x_boton = (ANCHO_PANTALLA - ancho_boton) // 2
    y_boton = 350
    rect_boton_inicio = pygame.Rect(x_boton, y_boton, ancho_boton, alto_boton)
    
    while True:
        pos_mouse = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "SALIR"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if rect_boton_inicio.collidepoint(pos_mouse):
                        return "JUEGO"

        # --- Dibujado ---
        # MODIFICADO: Dibujar el fondo primero
        if fondo_juego:
            pantalla.blit(fondo_juego, (0, 0))
        else:
            pantalla.fill(BLANCO) # Plan B si el fondo no carga
        
        # MODIFICADO: Texto en BLANCO para que resalte
        dibujar_texto("¡FISIRULETA!", fuente_titulo, BLANCO, pantalla, ANCHO_PANTALLA // 2, 200, centrado=True)
        dibujar_texto("Haz clic en 'Empezar' para jugar", fuente_opcion, BLANCO, pantalla, ANCHO_PANTALLA // 2, 250, centrado=True)

        # (El botón no necesita cambios, sus colores resaltan bien)
        color_actual_boton = COLOR_BOTON_NORMAL
        if rect_boton_inicio.collidepoint(pos_mouse):
            color_actual_boton = COLOR_BOTON_HOVER
        pygame.draw.rect(pantalla, color_actual_boton, rect_boton_inicio, border_radius=15)
        dibujar_texto("Empezar", fuente_pregunta, BLANCO, pantalla, rect_boton_inicio.centerx, rect_boton_inicio.centery, centrado=True)

        pygame.display.flip()
        clock.tick(FPS)

def pantalla_ruleta(categorias_disponibles, hud_data, iconos_grandes, iconos_hud, overlay, ruleta_imagen_base, fondo_ruleta):
    """
    MODIFICADO: Acepta y dibuja el fondo_ruleta.
    """
    estado_ruleta = "LISTO"
    tiempo_inicio_giro = 0
    tiempo_inicio_resultado = 0
    categoria_final = ""
    
    rect_boton_girar = pygame.Rect(ANCHO_PANTALLA // 2 - 125, 450, 250, 70)
    
    angulo_rotacion_FLECHA = 0
    velocidad_giro = 0
    duracion_giro_ms = 0
    
    flecha_base_surf = pygame.Surface((180, 20), pygame.SRCALPHA)
    pygame.draw.polygon(flecha_base_surf, ROJO_INCORRECTO, 
                        ((180, 10), (150, 0), (150, 20)))
    pygame.draw.rect(flecha_base_surf, ROJO_INCORRECTO, (0, 5, 150, 10))
    
    CENTRO_RULETA = (ANCHO_PANTALLA // 2, 300)

    secciones_ruleta = {
        "Corriente": (0, 120),
        "Campo Electrico": (120, 240),
        "Temperatura": (240, 360)
    }
    
    while True:
        pos_mouse = pygame.mouse.get_pos()
        tiempo_actual = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "SALIR"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if estado_ruleta == "LISTO" and rect_boton_girar.collidepoint(pos_mouse):
                        estado_ruleta = "GIRANDO"
                        tiempo_inicio_giro = tiempo_actual
                        velocidad_giro = random.uniform(20, 30)
                        duracion_giro_ms = random.uniform(2500, 4500)
                        print("¡Flecha girando!")

        if estado_ruleta == "GIRANDO":
            angulo_rotacion_FLECHA = (angulo_rotacion_FLECHA - velocidad_giro) % 360
            
            if tiempo_actual - tiempo_inicio_giro > duracion_giro_ms:
                estado_ruleta = "RESULTADO"
                tiempo_inicio_resultado = tiempo_actual
                angulo_final = angulo_rotacion_FLECHA % 360
                print(f"Giro detenido. Ángulo final de la flecha: {angulo_final}")
                
                categoria_final = ""
                for categoria, (min_angle, max_angle) in secciones_ruleta.items():
                    if min_angle <= angulo_final < max_angle:
                        categoria_final = categoria
                        break
                
                if not categoria_final:
                    categoria_final = "Corriente" 
                
                if categoria_final not in categorias_disponibles:
                    print(f"Categoría '{categoria_final}' no disponible, eligiendo otra.")
                    categoria_final = random.choice(categorias_disponibles)
                
                print(f"Resultado: {categoria_final}")

        elif estado_ruleta == "RESULTADO":
            duracion_resultado_ms = 2000
            if tiempo_actual - tiempo_inicio_resultado > duracion_resultado_ms:
                return categoria_final

        # --- Dibujado (Ruleta) ---
        # MODIFICADO: Dibujar el fondo primero
        if fondo_ruleta:
            pantalla.blit(fondo_ruleta, (0, 0))
        else:
            pantalla.fill(BLANCO)
        
        dibujar_texto("Gira la Ruleta", fuente_titulo, BLANCO, pantalla, ANCHO_PANTALLA // 2, 100, centrado=True)
        
        if ruleta_imagen_base:
            # 1. DIBUJAR LA RULETA (ESTÁTICA)
            rect_ruleta = ruleta_imagen_base.get_rect(center=CENTRO_RULETA)
            pantalla.blit(ruleta_imagen_base, rect_ruleta)
            
            # 2. DIBUJAR LA FLECHA (GIRANDO)
            flecha_rotada = pygame.transform.rotate(flecha_base_surf, angulo_rotacion_FLECHA)
            rect_flecha_rotada = flecha_rotada.get_rect(center=CENTRO_RULETA)
            pantalla.blit(flecha_rotada, rect_flecha_rotada)
            
            # 3. DIBUJAR UN CÍRCULO CENTRAL
            pygame.draw.circle(pantalla, GRIS_OSCURO, CENTRO_RULETA, 20)
            pygame.draw.circle(pantalla, GRIS_CLARO, CENTRO_RULETA, 15)

        else: # Plan B si la imagen no cargó
            rect_indicador = pygame.Rect(ANCHO_PANTALLA // 2 - 200, 200, 400, 150)
            pygame.draw.rect(pantalla, GRIS_CLARO, rect_indicador, 5, border_radius=10)
        
        
        if estado_ruleta == "LISTO":
            color_actual_boton = COLOR_BOTON_NORMAL
            if rect_boton_girar.collidepoint(pos_mouse):
                color_actual_boton = COLOR_BOTON_HOVER
            pygame.draw.rect(pantalla, color_actual_boton, rect_boton_girar, border_radius=15)
            dibujar_texto("GIRAR", fuente_pregunta, BLANCO, pantalla, rect_boton_girar.centerx, rect_boton_girar.centery, centrado=True)
        
        elif estado_ruleta == "RESULTADO":
             # MODIFICADO: Texto en blanco para que resalte
             dibujar_texto(f"¡Toca {categoria_final}!", fuente_pregunta, BLANCO, pantalla, ANCHO_PANTALLA // 2, 480, centrado=True)

        # Dibujar el HUD (siempre encima)
        dibujar_hud(pantalla, hud_data, iconos_hud, overlay)

        pygame.display.flip()
        clock.tick(FPS)

def pantalla_juego(pregunta_actual, hud_data, iconos_grandes, iconos_hud, overlay, fondo_juego):
    """
    MODIFICADO: Añadido un temporizador de 10 segundos y dibuja el fondo de juego.
    """
    running = True
    rects_opciones = []
    
    pos_y_pregunta = 250
    pos_y_opcion_base = 320
    
    espacio_opcion = 70
    estado_respuesta = None 
    tiempo_feedback = 0
    opcion_seleccionada = -1
    resultado_final = "INCORRECTO" 

    icono_categoria = iconos_grandes.get(pregunta_actual["categoria"], None)
    
    LIMITE_TIEMPO_MS = 10000 
    tiempo_inicio_pregunta = pygame.time.get_ticks() 
    tiempo_restante_segundos = 10 
    
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "SALIR"
            
            if event.type == pygame.MOUSEBUTTONDOWN and estado_respuesta is None:
                if event.button == 1:
                    pos_mouse = event.pos
                    
                    for i, rect in enumerate(rects_opciones):
                        if rect.collidepoint(pos_mouse):
                            opcion_seleccionada = i
                            if i == pregunta_actual['correcta']:
                                estado_respuesta = 'CORRECTO'
                                resultado_final = 'CORRECTO'
                            else:
                                estado_respuesta = 'INCORRECTO'
                                resultado_final = 'INCORRECTO'
                            
                            tiempo_feedback = pygame.time.get_ticks() 
                            
        if estado_respuesta is not None:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - tiempo_feedback > 1500: 
                return resultado_final 
        
        else:
            tiempo_actual = pygame.time.get_ticks()
            tiempo_transcurrido = tiempo_actual - tiempo_inicio_pregunta
            tiempo_restante_ms = LIMITE_TIEMPO_MS - tiempo_transcurrido
            
            tiempo_restante_segundos = max(0, int(tiempo_restante_ms / 1000) + 1)
            
            if tiempo_restante_ms <= 0:
                print("¡Se acabó el tiempo!")
                estado_respuesta = 'INCORRECTO'
                resultado_final = 'INCORRECTO'
                tiempo_feedback = pygame.time.get_ticks() 
                opcion_seleccionada = -1 

        # --- Dibujado (Render) ---
        # NUEVO: Dibujar el fondo primero
        if fondo_juego:
            pantalla.blit(fondo_juego, (0, 0))
        else:
            pantalla.fill(BLANCO) # Si no hay fondo, rellena con blanco
        
        # 1. Dibujar Categoría
        if icono_categoria:
            rect_icono = icono_categoria.get_rect(center=(ANCHO_PANTALLA // 2, 130))
            pantalla.blit(icono_categoria, rect_icono)
        
        dibujar_texto(pregunta_actual["categoria"], fuente_opcion, BLANCO, # Texto blanco
                      pantalla, ANCHO_PANTALLA // 2, 190, centrado=True)

        # 2. Dibujar el Temporizador
        color_timer = ROJO_INCORRECTO if (tiempo_restante_segundos <= 3 and estado_respuesta is None) else BLANCO # Texto blanco
        dibujar_texto(str(tiempo_restante_segundos), fuente_pregunta, color_timer, 
                      pantalla, ANCHO_PANTALLA // 2, 220, centrado=True)

        # 3. Dibujar Pregunta
        dibujar_texto(pregunta_actual["pregunta"], fuente_pregunta, BLANCO, # Texto blanco
                      pantalla, ANCHO_PANTALLA // 2, pos_y_pregunta, centrado=True)
        
        # 4. Dibujar Opciones
        rects_opciones.clear()
        for i, opcion in enumerate(pregunta_actual["opciones"]):
            pos_y = pos_y_opcion_base + (i * espacio_opcion)
            rect_boton = pygame.Rect(ANCHO_PANTALLA // 2 - 200, pos_y, 400, 50)
            rects_opciones.append(rect_boton)
            
            # Colores para que resalten en el fondo
            color_fondo_boton = (40, 40, 40, 200) # Fondo oscuro semitransparente
            color_borde_boton = BLANCO      
            color_texto_opcion = BLANCO     
            
            if estado_respuesta is not None:
                if i == opcion_seleccionada:
                    color_fondo_boton = VERDE_CORRECTO if estado_respuesta == 'CORRECTO' else ROJO_INCORRECTO
                if estado_respuesta == 'INCORRECTO' and i == pregunta_actual['correcta']:
                     color_fondo_boton = VERDE_CORRECTO
            
            # Dibujar el rectángulo del botón
            pygame.draw.rect(pantalla, color_fondo_boton, rect_boton, border_radius=10)
            pygame.draw.rect(pantalla, color_borde_boton, rect_boton, 2, border_radius=10) # Borde
            dibujar_texto(opcion, fuente_opcion, color_texto_opcion, pantalla, rect_boton.centerx, rect_boton.centery, centrado=True)

        # 5. Dibujar HUD
        dibujar_hud(pantalla, hud_data, iconos_hud, overlay)

        pygame.display.flip()
        clock.tick(FPS)

def pantalla_elegir_personaje(personajes_obtenidos, iconos_grandes):
    """
    Pantalla para elegir un personaje (quesito) al alcanzar
    la racha de 3.
    """
    
    rects_personajes = {}
    
    # Filtramos solo los personajes que AÚN NO se han obtenido
    personajes_elegibles = [p for p in LISTA_PERSONAJES if not personajes_obtenidos[p]]
    
    # Si por alguna razón entramos aquí sin nada que elegir, salimos
    if not personajes_elegibles:
        return None # Devolvemos None para que main sepa que no hubo elección

    while True:
        pos_mouse = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "SALIR"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Comprobamos clic en los botones
                    for personaje, rect in rects_personajes.items():
                        if rect.collidepoint(pos_mouse):
                            print(f"Personaje elegido: {personaje}")
                            return personaje # Devolvemos el nombre del personaje

        # --- Dibujado ---
        pantalla.fill(BLANCO)
        
        dibujar_texto("¡Racha de 3!", fuente_titulo, VERDE_CORRECTO, pantalla, ANCHO_PANTALLA // 2, 80, centrado=True)
        dibujar_texto("Elige un personaje", fuente_pregunta, NEGRO, pantalla, ANCHO_PANTALLA // 2, 150, centrado=True)

        rects_personajes.clear()
        pos_y_actual = 220
        
        # Mostramos TODOS los personajes
        for personaje in LISTA_PERSONAJES:
            # Botones más altos (120px) para los iconos (100x100)
            rect_boton = pygame.Rect(ANCHO_PANTALLA // 2 - 200, pos_y_actual, 400, 120)
            color_fondo = COLOR_CATEGORIAS.get(personaje, "DEFAULT")
            
            if personaje in personajes_elegibles:
                # Efecto Hover si es elegible
                if rect_boton.collidepoint(pos_mouse):
                    color_fondo = pygame.Color(color_fondo).lerp(BLANCO, 0.3) # Aclara el color
                
                # Guardamos el rect SÓLO si es elegible
                rects_personajes[personaje] = rect_boton
                pygame.draw.rect(pantalla, color_fondo, rect_boton, border_radius=15)
            
            else:
                # Si ya está obtenido, lo mostramos gris/desactivado
                pygame.draw.rect(pantalla, GRIS_CLARO, rect_boton, border_radius=15)
            
            # Dibujar icono (100x100) y texto dentro del botón
            icono = iconos_grandes.get(personaje, None)
            
            if icono:
                # Dibujamos el icono a la izquierda, centrado verticalmente
                rect_icono = icono.get_rect(midleft = (rect_boton.left + 20, rect_boton.centery))
                pantalla.blit(icono, rect_icono)

            # Dibujamos el texto a la derecha del icono
            color_texto = NEGRO if personaje in personajes_elegibles else GRIS_OSCURO
            dibujar_texto(personaje, 
                          fuente_opcion, 
                          color_texto, 
                          pantalla, 
                          rect_boton.left + 135, # Posición X (a la derecha del icono de 100px)
                          rect_boton.centery, # Posición Y (centrada)
                          centrado=False) # Alineado a la izquierda

            pos_y_actual += 140 # Más espacio entre botones (120 de alto + 20 de padding)

        pygame.display.flip()
        clock.tick(FPS)

def pantalla_victoria(iconos_grandes, fondo_victoria):
    """
    MODIFICADO: Dibuja el fondo de victoria y ajusta el color del texto.
    """
    
    ancho_boton = 300
    alto_boton = 70
    x_boton = (ANCHO_PANTALLA - ancho_boton) // 2
    y_boton = 500 # Lo subí un poco
    rect_boton_menu = pygame.Rect(x_boton, y_boton, ancho_boton, alto_boton)
    
    # Asegúrate de tener este color en tus constantes
    COLOR_TITULO_VICTORIA = (255, 223, 0) # Dorado
    
    while True:
        pos_mouse = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "SALIR"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if rect_boton_menu.collidepoint(pos_mouse):
                        return "INICIO"

        # --- Dibujado ---
        # NUEVO: Dibujar el fondo primero
        if fondo_victoria:
            pantalla.blit(fondo_victoria, (0, 0))
        else:
            pantalla.fill(BLANCO)
        
        # Título de Victoria
        dibujar_texto("¡FELICIDADES!", 
                      fuente_titulo, 
                      COLOR_TITULO_VICTORIA, 
                      pantalla, 
                      ANCHO_PANTALLA // 2, 80, 
                      centrado=True)
        
        dibujar_texto("¡Conseguiste los 3 personajes!", 
                      fuente_pregunta, 
                      BLANCO, # Texto blanco
                      pantalla, 
                      ANCHO_PANTALLA // 2, 180, # Más espacio
                      centrado=True)
        

        # --- Dibujar el botón "Volver al Menú" ---
        color_actual_boton = COLOR_BOTON_NORMAL
        if rect_boton_menu.collidepoint(pos_mouse):
            color_actual_boton = COLOR_BOTON_HOVER

        pygame.draw.rect(pantalla, color_actual_boton, rect_boton_menu, border_radius=15)
        
        dibujar_texto("Volver al Menu", 
                      fuente_opcion, 
                      BLANCO, 
                      pantalla, 
                      rect_boton_menu.centerx, rect_boton_menu.centery, 
                      centrado=True)

        pygame.display.flip()
        clock.tick(FPS)

# --- 7. Bucle Principal (Gestor de Estados) ---

def main():
    """
    MODIFICADO: El gestor de estados ahora incluye el estado "PREGUNTA_FINAL".
    """
    
    # Carga las preguntas normales
    lista_total_preguntas = cargar_preguntas("preguntas.json")
    if not lista_total_preguntas:
        print("No se pudieron cargar las preguntas. Saliendo.")
        pygame.quit()
        sys.exit()
    banco_preguntas_master = organizar_preguntas_por_categoria(lista_total_preguntas)
    
    # NUEVO: Carga las preguntas finales
    banco_preguntas_finales = cargar_preguntas_finales("preguntas_finales.json")
    if not banco_preguntas_finales:
        print("No se pudieron cargar las preguntas finales. Saliendo.")
        pygame.quit()
        sys.exit()

    # Carga todos los recursos gráficos
    iconos_grandes, iconos_hud, overlay_desactivado, ruleta_imagen_base, fondo_juego, fondo_victoria, fondo_ruleta = cargar_iconos()
    
    # Variables de estado de la partida
    puntuacion_total = 0
    racha_correctas = 0
    personajes_obtenidos = {personaje: False for personaje in LISTA_PERSONAJES}
    preguntas_disponibles_partida = {}
    
    estado_actual = "INICIO"
    pregunta_seleccionada = None
    personaje_a_ganar = None
    
    while estado_actual != "SALIR":
        
        hud_data = {
            "puntuacion": puntuacion_total,
            "racha": racha_correctas,
            "personajes": personajes_obtenidos
        }

        if estado_actual == "INICIO":
            resultado_inicio = pantalla_inicio(fondo_juego)
            
            if resultado_inicio == "JUEGO":
                preguntas_disponibles_partida = copy.deepcopy(banco_preguntas_master)
                puntuacion_total = 0
                racha_correctas = 0
                personajes_obtenidos = {p: False for p in LISTA_PERSONAJES}
                
                print("--- ¡Inicia nueva partida! ---")
                estado_actual = "RULETA"
            else: 
                estado_actual = "SALIR"
        
        elif estado_actual == "RULETA":
            categorias_disponibles = [cat for cat in preguntas_disponibles_partida if preguntas_disponibles_partida[cat]]
            
            if not categorias_disponibles:
                print("¡Se acabaron todas las preguntas del juego!")
                estado_actual = "INICIO"
                continue

            resultado_ruleta = pantalla_ruleta(categorias_disponibles, 
                                               hud_data, 
                                               iconos_grandes, 
                                               iconos_hud, 
                                               overlay_desactivado, 
                                               ruleta_imagen_base,
                                               fondo_ruleta)
            
            if resultado_ruleta == "SALIR":
                estado_actual = "SALIR"
            else:
                categoria_elegida = resultado_ruleta
                pregunta_seleccionada = preguntas_disponibles_partida[categoria_elegida].pop()
                estado_actual = "JUEGO"

        elif estado_actual == "JUEGO":
            resultado_juego = pantalla_juego(pregunta_seleccionada, 
                                             hud_data, 
                                             iconos_grandes, 
                                             iconos_hud, 
                                             overlay_desactivado,
                                             fondo_juego)
            
            if resultado_juego == "SALIR":
                estado_actual = "SALIR"
            
            elif resultado_juego == "CORRECTO":
                puntuacion_total += 1
                racha_correctas += 1
                print(f"¡Correcto! Racha: {racha_correctas}")
                
                if racha_correctas == 3:
                    print("¡Racha de 3! Pasando a elegir personaje.")
                    estado_actual = "ELEGIR_PERSONAJE"
                else:
                    estado_actual = "RULETA"
                    
            elif resultado_juego == "INCORRECTO":
                racha_correctas = 0
                print("Incorrecto. Racha reiniciada.")
                estado_actual = "RULETA"
        
        elif estado_actual == "ELEGIR_PERSONAJE":
            personaje_elegido = pantalla_elegir_personaje(personajes_obtenidos, iconos_grandes)
            
            if personaje_elegido == "SALIR":
                estado_actual = "SALIR"
            elif personaje_elegido: 
                personaje_a_ganar = personaje_elegido
                estado_actual = "PREGUNTA_FINAL"
                print(f"Intentando ganar a {personaje_a_ganar}...")
            else:
                racha_correctas = 0
                estado_actual = "RULETA"
        
        elif estado_actual == "PREGUNTA_FINAL":
            
            # --- ¡AQUÍ ESTÁ EL CAMBIO! ---
            # 1. Obtener la LISTA de preguntas especiales
            lista_preguntas_especiales = banco_preguntas_finales[personaje_a_ganar]
            # 2. Elegir una al azar de esa lista
            pregunta_especial = random.choice(lista_preguntas_especiales)
            # --- FIN DEL CAMBIO ---
            
            # 3. Reutilizamos la pantalla_juego para mostrar esta pregunta
            resultado_juego = pantalla_juego(pregunta_especial, 
                                             hud_data, 
                                             iconos_grandes, 
                                             iconos_hud, 
                                             overlay_desactivado,
                                             fondo_juego)
            
            # 4. Procesar el resultado
            if resultado_juego == "CORRECTO":
                print(f"¡CORRECTO! Has ganado a {personaje_a_ganar}.")
                personajes_obtenidos[personaje_a_ganar] = True
            
            elif resultado_juego == "INCORRECTO":
                print(f"¡INCORRECTO! No has ganado a {personaje_a_ganar}.")
            
            # 5. En cualquier caso, reiniciamos la racha y volvemos a la ruleta
            racha_correctas = 0
            personaje_a_ganar = None
            
            # 6. Comprobar si ahora ha ganado el juego
            if all(personajes_obtenidos.values()):
                print("¡HAS GANADO! ¡Obtuviste todos los personajes!")
                estado_actual = "VICTORIA"
            else:
                estado_actual = "RULETA"
        
        elif estado_actual == "VICTORIA":
            resultado_victoria = pantalla_victoria(iconos_grandes, fondo_victoria)
            
            if resultado_victoria == "INICIO":
                estado_actual = "INICIO"
            else: 
                estado_actual = "SALIR"

    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main()