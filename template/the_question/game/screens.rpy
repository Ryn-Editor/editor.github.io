# screens.rpy
# Sistema híbrido de menús para RynEditor
# Combina menús por defecto de Ren'Py con personalización por imágenes

################################################################################
## Pantallas por Defecto de Ren'Py
################################################################################

# Pantalla de diálogo
screen say(who, what):
    style_prefix "say"

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "namebox"
                text who id "who"

        text what id "what"

# Pantalla de entrada de texto
screen input(prompt):
    style_prefix "input"

    window:

        vbox:
            text prompt style "input_prompt"
            input id "input"

# Pantalla de elección
screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action

# Pantalla de menú rápido
screen quick_menu():

    zorder 100

    if quick_menu:

        hbox:
            style_prefix "quick"

            xalign 0.5
            yalign 1.0

            textbutton _("Atrás") action Rollback()
            textbutton _("Historial") action ShowMenu('history')
            textbutton _("Saltar") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Auto") action Preference("auto-forward", "toggle")
            textbutton _("Guardar") action ShowMenu('save')
            textbutton _("Cargar") action ShowMenu('load')
            textbutton _("Opciones") action ShowMenu('preferences')

# Pantalla de navegación
screen navigation():

    vbox:
        style_prefix "navigation"

        xpos gui.navigation_xpos
        yalign 0.5

        spacing gui.navigation_spacing

        if main_menu:

            textbutton _("Comenzar") action Start()

        else:

            textbutton _("Historial") action ShowMenu("history")

            textbutton _("Guardar") action ShowMenu("save")

        textbutton _("Cargar") action ShowMenu("load")

        textbutton _("Opciones") action ShowMenu("preferences")

        if _in_replay:

            textbutton _("Finalizar Replay") action EndReplay(confirm=True)

        elif not main_menu:

            textbutton _("Menú Principal") action MainMenu()

        textbutton _("Acerca de") action ShowMenu("about")

        if renpy.variant("pc"):

            textbutton _("Ayuda") action ShowMenu("help")

            textbutton _("Salir") action Quit(confirm=not main_menu)

# Pantalla de menú principal
screen main_menu():

    tag menu

    add gui.main_menu_background

    frame:
        style "main_menu_frame"

    use navigation

    if gui.show_name:

        vbox:
            style "main_menu_vbox"

            text "[config.name!t]":
                style "main_menu_title"

            text "[config.version]":
                style "main_menu_version"

# Pantalla de juego
screen game_menu(title, scroll=None, yinitial=0.0):

    style_prefix "game_menu"

    if main_menu:
        add gui.main_menu_background
    else:
        add gui.game_menu_background

    frame:
        style "game_menu_outer_frame"

        hbox:

            frame:
                style "game_menu_navigation_frame"

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":

                    viewport:
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True

                        side_yfill True

                        vbox:
                            transclude

                elif scroll == "vpgrid":

                    vpgrid:
                        cols 1
                        yinitial yinitial

                        scrollbars "vertical"
                        mousewheel True
                        draggable True

                        side_yfill True

                        transclude

                else:

                    transclude

    use navigation

    textbutton _("Regresar"):
        style "return_button"

        action Return()

    label title

# Pantalla de confirmación
screen confirm(message, yes_action, no_action):

    modal True

    zorder 200

    style_prefix "confirm"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 30

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 100

                textbutton _("Sí") action yes_action
                textbutton _("No") action no_action

    key "game_menu" action no_action

# Pantalla de guardar
screen save():

    tag menu

    use file_slots(_("Guardar"))

# Pantalla de cargar
screen load():

    tag menu

    use file_slots(_("Cargar"))

# Pantalla de slots de archivo
screen file_slots(title):

    default page_name_value = FilePageNameInputValue()

    use game_menu(title):

        fixed:

            order_reverse True

            button:
                style "page_label"

                key_events True
                xalign 0.5
                action page_name_value.Toggle()

                input:
                    style "page_label_text"
                    value page_name_value

            grid gui.file_slot_cols gui.file_slot_rows:
                style "slot_grid"

                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    button:
                        action FileAction(slot)

                        has vbox

                        add FileScreenshot(slot) xalign 0.5

                        text FileTime(slot, format=_("{#file_time}%A, %d de %B %Y, %H:%M"), empty=_("slot vacío")):
                            style "slot_time_text"

                        text FileSaveName(slot):
                            style "slot_name_text"

                        key "save_delete" action FileDelete(slot)

            hbox:
                style_prefix "page"

                xalign 0.5
                yalign 1.0

                spacing gui.page_spacing

                textbutton _("<") action FilePagePrevious()

                if config.has_autosave:
                    textbutton _("{#auto_page}A") action FilePage("auto")

                if config.has_quicksave:
                    textbutton _("{#quick_page}R") action FilePage("quick")

                for page in range(1, 10):
                    textbutton "[page]" action FilePage(page)

                textbutton _(">") action FilePageNext()

# Pantalla de preferencias
screen preferences():

    tag menu

    use game_menu(_("Opciones")):

        vbox:

            hbox:
                box_wrap True

                if renpy.variant("pc"):

                    vbox:
                        style_prefix "radio"
                        label _("Pantalla")
                        textbutton _("Ventana") action Preference("display", "window")
                        textbutton _("Pantalla Completa") action Preference("display", "fullscreen")

                vbox:
                    style_prefix "radio"
                    label _("Deshacer")
                    textbutton _("Deshabilitado") action Preference("rollback side", "disable")
                    textbutton _("Izquierda") action Preference("rollback side", "left")
                    textbutton _("Derecha") action Preference("rollback side", "right")

                vbox:
                    style_prefix "check"
                    label _("Saltar")
                    textbutton _("Texto no visto") action Preference("skip", "toggle")
                    textbutton _("Después de elecciones") action Preference("after choices", "toggle")
                    textbutton _("Transiciones") action Preference("transitions", "toggle")

                vbox:
                    style_prefix "radio"
                    label _("Velocidad de Auto")
                    textbutton _("Lento") action Preference("auto-forward time", 0.0)
                    textbutton _("Normal") action Preference("auto-forward time", 0.0)
                    textbutton _("Rápido") action Preference("auto-forward time", 0.0)

            null height (4 * gui.pref_spacing)

            hbox:
                style_prefix "slider"
                box_wrap True

                vbox:

                    label _("Velocidad de Texto")

                    bar value Preference("text speed")

                    label _("Velocidad de Auto")

                    bar value Preference("auto-forward time")

                vbox:

                    if config.has_music:
                        label _("Volumen de Música")

                        hbox:
                            bar value Preference("music volume")

                    if config.has_sound:

                        label _("Volumen de Sonido")

                        hbox:
                            bar value Preference("sound volume")

                            if config.sample_sound:
                                textbutton _("Probar") action Play("sound", config.sample_sound)

                    if config.has_voice:
                        label _("Volumen de Voz")

                        hbox:
                            bar value Preference("voice volume")

                            if config.sample_voice:
                                textbutton _("Probar") action Play("voice", config.sample_voice)

                    if config.has_music or config.has_sound or config.has_voice:
                        null height gui.pref_spacing

                        textbutton _("Silenciar Todo"):
                            action Preference("all mute", "toggle")
                            style "mute_all_button"

# Pantalla de historial
screen history():

    tag menu

    predict False

    use game_menu(_("Historial"), scroll=("vpgrid" if gui.history_height else "viewport"), yinitial=1.0):

        style_prefix "history"

        for h in _history_list:

            window:

                has fixed:
                    yfit True

                if h.who:

                    label h.who:
                        style "history_name"

                        if "color" in h.who_args:
                            text_color h.who_args["color"]

                text h.what

        if not _history_list:
            label _("El historial de diálogo está vacío.")

# Pantalla de ayuda
screen help():

    tag menu

    default device = "keyboard"

    use game_menu(_("Ayuda")):

        style_prefix "help"

        vbox:
            spacing 15

            hbox:

                textbutton _("Teclado") action SetScreenVariable("device", "keyboard")
                textbutton _("Ratón") action SetScreenVariable("device", "mouse")

                if renpy.variant("pc"):

                    textbutton _("Mando") action SetScreenVariable("device", "gamepad")

            if device == "keyboard":
                use keyboard_help
            elif device == "mouse":
                use mouse_help
            elif device == "gamepad":
                use gamepad_help

# Pantalla de ayuda del teclado
screen keyboard_help():

    hbox:
        label _("Enter")
        text _("Avanza el diálogo y activa la interfaz.")

    hbox:
        label _("Espacio")
        text _("Avanza el diálogo sin activar las opciones.")

    hbox:
        label _("Flechas")
        text _("Navega por la interfaz.")

    hbox:
        label _("Escape")
        text _("Accede al menú del juego.")

    hbox:
        label _("Ctrl")
        text _("Salta el diálogo mientras se mantiene presionado.")

    hbox:
        label _("Tab")
        text _("Activa/desactiva el salto de diálogo.")

    hbox:
        label _("Página Arriba")
        text _("Retrocede al diálogo anterior.")

    hbox:
        label _("Página Abajo")
        text _("Avanza al diálogo siguiente.")

    hbox:
        label "H"
        text _("Oculta la interfaz de usuario.")

    hbox:
        label "S"
        text _("Toma una captura de pantalla.")

    hbox:
        label "V"
        text _("Activa/desactiva la asistencia {a=https://www.renpy.org/l/voicing}por voz{/a}.")

    hbox:
        label "Shift+A"
        text _("Abre el menú de accesibilidad.")

# Pantalla de ayuda del ratón
screen mouse_help():

    hbox:
        label _("Clic Izquierdo")
        text _("Avanza el diálogo y activa la interfaz.")

    hbox:
        label _("Clic Medio")
        text _("Oculta la interfaz de usuario.")

    hbox:
        label _("Clic Derecho")
        text _("Accede al menú del juego.")

    hbox:
        label _("Rueda del Ratón Arriba")
        text _("Retrocede al diálogo anterior.")

    hbox:
        label _("Rueda del Ratón Abajo")
        text _("Avanza al diálogo siguiente.")

# Pantalla de ayuda del mando
screen gamepad_help():

    hbox:
        label _("Gatillo Derecho\nA/Botón Inferior")
        text _("Avanza el diálogo y activa la interfaz.")

    hbox:
        label _("Gatillo Izquierdo\nGatillo Superior")
        text _("Retrocede al diálogo anterior.")

    hbox:
        label _("D-Pad")
        text _("Navega por la interfaz.")

    hbox:
        label _("Palo Derecho")
        text _("Navega por la interfaz.")

    hbox:
        label _("A/Botón Inferior")
        text _("Avanza el diálogo y activa la interfaz.")

    hbox:
        label _("B/Botón Derecho")
        text _("Accede al menú del juego.")

    hbox:
        label _("X/Botón Superior")
        text _("Activa/desactiva el salto de diálogo.")

    hbox:
        label _("Y/Botón Izquierdo")
        text _("Oculta la interfaz de usuario.")

    hbox:
        label _("Palo Izquierdo")
        text _("Avanza al diálogo siguiente.")

    hbox:
        label _("Palo Derecho")
        text _("Avanza al diálogo siguiente.")

    hbox:
        label _("Botón Inicio")
        text _("Accede al menú del juego.")

    hbox:
        label _("Botón Seleccionar")
        text _("Activa/desactiva el salto de diálogo.")

# Pantalla de acerca de
screen about():

    tag menu

    use game_menu(_("Acerca de")):

        style_prefix "about"

        vbox:

            label "[config.name!t]"
            text _("Versión [config.version!t]\n")

            if gui.about:
                text "[gui.about!t]\n"

            text _("Hecho con {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n[renpy.license!t]")

# Pantalla de confirmación de salida
screen confirm_quit():

    modal True

    zorder 200

    style_prefix "confirm"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 30

            label _("¿Está seguro de que desea salir?") style "confirm_prompt" xalign 0.5

            hbox:
                xalign 0.5
                spacing 100

                textbutton _("Sí") action Quit(confirm=False)
                textbutton _("No") action Return()

    key "game_menu" action Return()

################################################################################
## SISTEMA HÍBRIDO DE PERSONALIZACIÓN
################################################################################

# Sistema de detección automática
init python:
    def has_custom_images():
        """Detecta si hay imágenes personalizadas disponibles"""
        return (
            renpy.exists("images/menus/main_menu_bg.png") or
            renpy.exists("images/buttons/start_idle.png") or
            renpy.exists("images/interface/textbox.png") or
            renpy.exists("images/buttons/back_idle.png")
        )
    
    def use_custom_menus():
        """Determina si usar menús personalizados con imágenes"""
        return has_custom_images() and gui.custom_menus_enabled
    
    def use_custom_interface():
        """Determina si usar interfaz personalizada"""
        return has_custom_images() and gui.custom_interface_enabled
    
    def use_custom_extras():
        """Determina si usar extras personalizados"""
        return has_custom_images() and gui.custom_extras_enabled

# ===== MENÚS PERSONALIZADOS CON IMÁGENES =====
# Solo se activan si hay imágenes disponibles

if use_custom_menus():
    # Redefinir main_menu con imágenes personalizadas
    screen main_menu():
        tag menu
        add "main_menu_bg"
        
        # Logo
        add "logo"
        
        # Botones con imágenes
        imagebutton:
            idle "start_button_idle"
            hover "start_button_hover"
            focus_mask "images/buttons/start_button_hitbox.png"
            action Start()
        
        imagebutton:
            idle "load_button_idle"
            hover "load_button_hover"
            focus_mask "images/buttons/load_button_hitbox.png"
            action ShowMenu("load")
        
        imagebutton:
            idle "preferences_button_idle"
            hover "preferences_button_hover"
            focus_mask "images/buttons/preferences_button_hitbox.png"
            action ShowMenu("preferences")
        
        imagebutton:
            idle "extras_button_idle"
            hover "extras_button_hover"
            focus_mask "images/buttons/extras_button_hitbox.png"
            action ShowMenu("extras")
        
        imagebutton:
            idle "quit_button_idle"
            hover "quit_button_hover"
            focus_mask "images/buttons/quit_button_hitbox.png"
            action Quit(confirm="¿Está seguro de que desea abandonar este mundo? La historia quedará en suspenso.")
        
        # Botones sociales
        imagebutton:
            idle "discord_button"
            focus_mask True
            style "social_media_image_button"
            action OpenURL("https://discord.gg/tu_servidor")
        
        imagebutton:
            idle "patreon_button"
            focus_mask True
            style "social_media_image_button"
            action OpenURL("https://www.patreon.com/tu_usuario")
        
        # Botón de editor visual
        textbutton "Editor Visual":
            action Show("visual_editor")
            xalign 0.5
            yalign 0.8

    # Redefinir preferences con imágenes personalizadas
    screen preferences():
        tag menu
        add "prefs_menu_bg"
        add "prefs_logo"
        add "fullscreen_logo"
        
        # Botón para fullscreen
        imagebutton:
            idle "fullscreen_button_idle"
            hover "fullscreen_button_hover"
            selected_idle "fullscreen_button_done"
            selected_hover "fullscreen_button_hover"
            focus_mask True
            action Preference("display", "fullscreen")
        
        # Botón para window mode
        imagebutton:
            idle "window_button_idle"
            hover "window_button_hover"
            selected_idle "window_button_done"
            selected_hover "window_button_hover"
            focus_mask True
            action Preference("display", "window")
        
        # Botón de regreso
        imagebutton:
            idle "back_button_idle"
            hover "back_button_hover"
            focus_mask True
            action Return()
        
        # Slider para volumen música
        bar value Preference("music volume"):
            style "music_slider"

    # Redefinir save con imágenes personalizadas
    screen save():
        tag menu
        add "save_menu_bg"
        
        fixed:
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"
                spacing gui.slot_spacing
                xalign 0.5
                yalign 0.45
                
                for i in range(gui.file_slot_cols * gui.file_slot_rows):
                    $ slot = i + 1
                    button:
                        action FileAction(slot)
                        has vbox
                        add FileScreenshot(slot) xalign 0.5
                        text FileTime(slot, format=_("{#file_time}%A, %d de %B %Y, %H:%M"), empty=_("vacío")):
                            style "slot_time_text"
                        text FileSaveName(slot):
                            style "slot_name_text"
                        key "save_delete" action FileDelete(slot)
            
            hbox:
                style_prefix "page"
                xalign 0.5
                yalign 0.95
                spacing gui.page_spacing
                
                textbutton _("<") action FilePagePrevious()
                if config.has_autosave:
                    textbutton _("A") action FilePage("auto")
                if config.has_quicksave:
                    textbutton _("R") action FilePage("quick")
                for page in range(1, 10):
                    textbutton "[page]" action FilePage(page)
                textbutton _(">") action FilePageNext()
        
        # Botón de regreso personalizado
        imagebutton:
            idle "back_button_idle"
            hover "back_button_hover"
            focus_mask True
            action Return()

    # Redefinir load con imágenes personalizadas
    screen load():
        tag menu
        add "load_menu_bg"
        
        fixed:
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"
                spacing gui.slot_spacing
                xalign 0.5
                yalign 0.45
                
                for i in range(gui.file_slot_cols * gui.file_slot_rows):
                    $ slot = i + 1
                    button:
                        action FileAction(slot)
                        has vbox
                        add FileScreenshot(slot) xalign 0.5
                        text FileTime(slot, format=_("{#file_time}%A, %d de %B %Y, %H:%M"), empty=_("vacío")):
                            style "slot_time_text"
                        text FileSaveName(slot):
                            style "slot_name_text"
            
            hbox:
                style_prefix "page"
                xalign 0.5
                yalign 0.95
                spacing gui.page_spacing
                
                textbutton _("<") action FilePagePrevious()
                if config.has_autosave:
                    textbutton _("A") action FilePage("auto")
                if config.has_quicksave:
                    textbutton _("R") action FilePage("quick")
                for page in range(1, 10):
                    textbutton "[page]" action FilePage(page)
                textbutton _(">") action FilePageNext()
        
        # Botón de regreso personalizado
        imagebutton:
            idle "back_button_idle"
            hover "back_button_hover"
            focus_mask True
            action Return()

# ===== INTERFAZ PERSONALIZADA =====
# Solo se activa si hay imágenes disponibles

if use_custom_interface():
    # Redefinir pantalla de diálogo con interfaz personalizada
    screen say(who, what):
        fixed:
            add "interface_textbox"
            
            if who is not None:
                text who:
                    style "say_label"
                    xpos 402
                    ypos 850
            
            text what:
                id "what"
                style "say_dialogue"
                xpos 402
                ypos 900
                xsize 1116

    # Redefinir menú rápido con interfaz personalizada
    screen quick_menu():
        zorder 100
        
        if quick_menu:
            hbox:
                style_prefix "quick"
                xalign 0.5
                yalign 1.0
                yoffset -20
                spacing 15
                
                imagebutton:
                    idle "quick_button_back_idle"
                    hover "quick_button_back_hover"
                    action Rollback()
                
                imagebutton:
                    idle "quick_button_skip_idle"
                    hover "quick_button_skip_hover"
                    action Skip()
                
                imagebutton:
                    idle "quick_button_save_idle"
                    hover "quick_button_save_hover"
                    action ShowMenu('save')
                
                imagebutton:
                    idle "quick_button_load_idle"
                    hover "quick_button_load_hover"
                    action ShowMenu('load')
                
                imagebutton:
                    idle "quick_button_prefs_idle"
                    hover "quick_button_prefs_hover"
                    action ShowMenu('preferences')

    # Redefinir pantalla de confirmación con interfaz personalizada
    screen confirm(message, yes_action, no_action):
        modal True
        zorder 200
        
        fixed:
            add "confirm_frame_background"
            
            text message:
                style "confirm_prompt_text"
                xalign 0.5
                yalign 0.4
            
            hbox:
                xalign 0.5
                yalign 0.6
                spacing 100
                
                imagebutton idle "confirm_button_yes_idle" hover "confirm_button_yes_hover" action yes_action
                imagebutton idle "confirm_button_no_idle" hover "confirm_button_no_hover" action no_action
        
        key "game_menu" action no_action

    # Redefinir navegación con interfaz personalizada
    screen navigation():
        vbox:
            style_prefix "navigation"
            xpos gui.navigation_xpos
            yalign 0.5
            spacing gui.navigation_spacing
            
            if main_menu:
                textbutton _("Comenzar") action Start()
            else:
                textbutton _("Historial") action ShowMenu("history")
                textbutton _("Guardar") action ShowMenu("save")
            
            textbutton _("Cargar") action ShowMenu("load")
            textbutton _("Opciones") action ShowMenu("preferences")
            
            if not main_menu:
                textbutton _("Menú principal") action MainMenu(confirm="Si regresa al menú, el progreso no guardado se perderá en el éter. ¿Desea continuar?")
            
            textbutton _("Salir") action Quit(confirm="¿Está seguro de que desea abandonar este mundo? La historia quedará en suspenso.")

# ===== EXTRAS PERSONALIZADOS =====
# Solo se activa si hay imágenes disponibles

if use_custom_extras():
    # Pantalla de extras con galería y DLCs
    screen extras():
        tag menu
        default extras_page = "gallery"
        
        add "extras_menu_bg"
        
        hbox:
            xalign 0.5
            yalign 0.5
            spacing 50
            
            # Columna de navegación
            vbox:
                spacing 20
                
                # Botón para la galería
                imagebutton:
                    idle button_gallery_idle
                    hover button_gallery_hover
                    selected_idle button_gallery_selected
                    action SetScreenVariable("extras_page", "gallery")
                    selected (extras_page == "gallery")
                
                # Botón para DLCs
                imagebutton:
                    idle button_dlc_idle
                    hover button_dlc_hover
                    selected_idle button_dlc_selected
                    action SetScreenVariable("extras_page", "dlcs")
                    selected (extras_page == "dlcs")
            
            # Contenido
            frame:
                background Frame(Solid("#00000088"), 10, 10)
                xysize (1200, 700)
                
                if extras_page == "gallery":
                    use gallery_page
                elif extras_page == "dlcs":
                    use dlc_page
        
        # Botón de regreso
        imagebutton:
            idle "back_button_idle"
            hover "back_button_hover"
            action MainMenu()
            xalign 0.95 yalign 0.95

    # Pantalla de galería
    screen gallery_page():
        vpgrid:
            cols 5
            spacing 15
            xalign 0.5 yalign 0.5
            
            for img in persistent.unlocked_gallery:
                button:
                    action Show("image_viewer", image_to_show=img)
                    add img size (200, 112)

    # Pantalla de DLCs
    screen dlc_page():
        vbox:
            xalign 0.5 yalign 0.5 spacing 20
            text "Contenido Adicional" style "gui_label_text"
            if renpy.has_dlc("epilogue"):
                textbutton "Jugar Epílogo" action Start("dlc_epilogue_start")
            else:
                textbutton "Epílogo (No adquirido)" sensitive False

# ===== ESTILOS PERSONALIZADOS =====
# Estilos para elementos con imágenes

style social_media_image_button:
    background None
    padding (0, 0)
    margin (0, 0)
    xalign 0.95
    yalign 0.95

style music_slider:
    base_bar "images/sliders/music_base.png"
    thumb "images/sliders/music_thumb.png"
    xsize 600
    ysize 50

style custom_button:
    background None
    padding (0, 0)
    margin (0, 0)

# ===== CONFIGURACIÓN DE DETECCIÓN AUTOMÁTICA =====
# Variables de control del sistema híbrido

init python:
    # Configuración por defecto
    if not hasattr(gui, 'custom_menus_enabled'):
        gui.custom_menus_enabled = True
    if not hasattr(gui, 'custom_interface_enabled'):
        gui.custom_interface_enabled = True
    if not hasattr(gui, 'custom_extras_enabled'):
        gui.custom_extras_enabled = True
