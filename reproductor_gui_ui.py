import sys
import time
import vlc
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLineEdit, QLabel, QListWidget, QMessageBox,
    QTabWidget, QSplitter, QFrame, QProgressBar, QComboBox, QListWidgetItem,
    QSlider, QGroupBox, QCheckBox, QMainWindow
)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor, QPainter, QBrush, QLinearGradient
from PyQt5 import uic
from jellyfin_api import JellyfinAPI, DEFAULT_CONFIG
from config_ui import get_config, apply_config_to_window
from winamp_styles import apply_winamp_theme_to_window
from icon_helper import IconHelper, print_icon_status

class VisualizerWidget(QWidget):
    """Widget para simular el visualizador de Winamp"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(50)
        self.setMaximumHeight(80)
        self.setStyleSheet("background-color: #000000; border: 1px solid #404040;")
        self.bars = [random.randint(1, 20) for _ in range(32)]
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_visualizer)
        self.is_playing = False
    
    def start_animation(self):
        """Inicia la animación del visualizador"""
        self.is_playing = True
        self.timer.start(100)
        self.setVisible(True)
    
    def stop_animation(self):
        """Detiene la animación del visualizador"""
        self.is_playing = False
        self.timer.stop()
        self.setVisible(False)
        # Resetear barras a estado estático
        self.bars = [5 for _ in range(32)]
        self.update()
    
    def update_visualizer(self):
        """Actualiza el visualizador con datos aleatorios"""
        if not self.is_playing:
            return
            
        for i in range(len(self.bars)):
            if random.random() < 0.3:  # 30% de probabilidad de cambio
                self.bars[i] = random.randint(1, 25)
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Fondo negro
        painter.fillRect(self.rect(), QColor(0, 0, 0))
        
        # Dibujar barras del espectro
        bar_width = self.width() // len(self.bars)
        for i, height in enumerate(self.bars):
            x = i * bar_width
            bar_height = int((height / 25) * self.height())  # Convertir a int
            y = self.height() - bar_height
            
            # Gradiente verde como Winamp
            gradient = QLinearGradient(x, y, x, self.height())
            gradient.setColorAt(0, QColor(0, 255, 0))
            gradient.setColorAt(1, QColor(0, 128, 0))
            
            # Convertir todas las coordenadas a enteros
            painter.fillRect(int(x + 1), int(y), int(bar_width - 2), int(bar_height), QBrush(gradient))

class WorkerThread(QThread):
    """Hilo para cargar datos de Jellyfin sin bloquear la interfaz"""
    albums_loaded = pyqtSignal(list)
    songs_loaded = pyqtSignal(list)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, jellyfin_api):
        super().__init__()
        self.jellyfin_api = jellyfin_api
        self.task = None
        self.album_id = None
    
    def load_albums(self):
        self.task = "albums"
        self.start()
    
    def load_songs(self, album_id):
        self.task = "songs"
        self.album_id = album_id
        self.start()
    
    def run(self):
        try:
            if self.task == "albums":
                albums = self.jellyfin_api.listar_albumes()
                self.albums_loaded.emit(albums)
            elif self.task == "songs":
                songs = self.jellyfin_api.obtener_canciones_del_album(self.album_id)
                self.songs_loaded.emit(songs)
        except Exception as e:
            self.error_occurred.emit(str(e))

class ReproductorJellyfinUI(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Cargar configuración
        self.config = get_config()
        
        # Cargar la interfaz desde el archivo .ui
        uic.loadUi('main_window.ui', self)
        
        # Aplicar configuración
        apply_config_to_window(self)
        
        # Aplicar tema Winamp
        apply_winamp_theme_to_window(self)
        
        # Aplicar íconos del tema
        IconHelper.apply_theme_icons_to_window(self)
        
        # Mostrar estado de íconos en consola
        print_icon_status()
        
        # Inicializar variables
        self.jellyfin_api = JellyfinAPI(
            DEFAULT_CONFIG["JELLYFIN_URL"],
            DEFAULT_CONFIG["API_KEY"],
            DEFAULT_CONFIG["USER_ID"]
        )
        self.worker_thread = WorkerThread(self.jellyfin_api)
        self.worker_thread.albums_loaded.connect(self.on_albums_loaded)
        self.worker_thread.songs_loaded.connect(self.on_songs_loaded)
        self.worker_thread.error_occurred.connect(self.on_error)
        
        # Variables de reproducción
        self.instance = None
        self.player = None
        self.queue = []
        self.queue_info = []
        self.current_index = -1
        self.is_playing = False
        self.is_paused = False
        self.albums = []
        self.current_album_songs = []
        
        # Configurar el visualizador
        self.visualizer = VisualizerWidget()
        self.verticalLayout.addWidget(self.visualizer)
        
        # Configurar visualizador según configuración
        if not self.config["features"]["enable_visualizer"]:
            self.visualizer.setVisible(False)
        
        # Conectar señales
        self.connect_signals()
        
        # Configurar timer
        self.setup_timer()
        
        # Verificar VLC
        self.check_vlc_installation()
        
        # Probar conexión
        if self.config["interface"]["auto_connect"]:
            self.test_connection()
    
    def connect_signals(self):
        """Conecta todas las señales de la interfaz"""
        # Botones de control
        self.playButton.clicked.connect(self.reproducir_actual)
        self.pauseButton.clicked.connect(self.pausar)
        self.stopButton.clicked.connect(self.detener)
        self.prevButton.clicked.connect(self.anterior)
        self.nextButton.clicked.connect(self.siguiente)
        
        # Botones de álbum
        self.addAllButton.clicked.connect(self.agregar_todo_album)
        self.playAlbumButton.clicked.connect(self.reproducir_album)
        
        # Botones de cola
        self.clearQueueButton.clicked.connect(self.limpiar_cola)
        self.shuffleButton.clicked.connect(self.aleatorio)
        
        # Búsqueda y refresh
        self.searchInput.textChanged.connect(self.on_search_changed)
        self.refreshButton.clicked.connect(self.load_albums)
        
        # Listas
        self.albumsList.itemClicked.connect(self.on_album_selected)
        self.songsList.itemDoubleClicked.connect(self.on_song_double_clicked)
        self.queueList.itemDoubleClicked.connect(self.on_queue_item_double_clicked)
        
        # Controles de audio
        self.volumeSlider.valueChanged.connect(self.on_volume_changed)
        self.balanceSlider.valueChanged.connect(self.on_balance_changed)
    
    def check_vlc_installation(self):
        """Verifica si VLC está instalado"""
        try:
            self.instance = vlc.Instance()
            self.player = self.instance.media_player_new()
        except Exception as e:
            QMessageBox.critical(self, "Error VLC", 
                               f"Error al inicializar VLC: {str(e)}\n"
                               "Asegúrate de que VLC esté instalado.")
    
    def setup_timer(self):
        """Configura el timer para actualizar el tiempo de reproducción"""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_tiempo)
        self.timer.start(1000)
    
    def test_connection(self):
        """Prueba la conexión con Jellyfin"""
        if self.jellyfin_api.test_connection():
            self.statusLabel.setText("✅ Conectado a Jellyfin")
            self.load_albums()
        else:
            self.statusLabel.setText("❌ Error de conexión")
    
    def load_albums(self):
        """Carga la lista de álbumes"""
        self.statusLabel.setText("🔄 Cargando...")
        self.worker_thread.load_albums()
    
    def on_albums_loaded(self, albums):
        """Callback cuando se cargan los álbumes"""
        self.albums = albums
        self.albumsList.clear()
        
        for album in albums:
            display_text = f"{album['Nombre']} - {album['Artista']}"
            if album.get('Año'):
                display_text += f" ({album['Año']})"
            
            item = QListWidgetItem(display_text)
            item.setData(Qt.UserRole, album)
            self.albumsList.addItem(item)
        
        self.statusLabel.setText(f"✅ {len(albums)} álbumes")
    
    def on_album_selected(self, item):
        """Callback cuando se selecciona un álbum"""
        album = item.data(Qt.UserRole)
        self.albumInfoLabel.setText(f"{album['Nombre']} - {album['Artista']}")
        
        # Cargar canciones del álbum
        self.statusLabel.setText("🔄 Cargando canciones...")
        self.worker_thread.load_songs(album['Id'])
    
    def on_songs_loaded(self, songs):
        """Callback cuando se cargan las canciones"""
        self.current_album_songs = songs
        self.songsList.clear()
        
        for song in songs:
            display_text = f"{song['Numero']:02d}. {song['Titulo']} ({song['Duracion']})"
            item = QListWidgetItem(display_text)
            item.setData(Qt.UserRole, song)
            self.songsList.addItem(item)
        
        self.statusLabel.setText("✅ Listo")
    
    def on_song_double_clicked(self, item):
        """Callback cuando se hace doble clic en una canción"""
        song = item.data(Qt.UserRole)
        self.queue = [song['StreamUrl']]
        self.queue_info = [song]
        self.current_index = 0
        self.actualizar_lista_cola()
        self.reproducir_actual()
    
    def on_queue_item_double_clicked(self, item):
        """Callback cuando se hace doble clic en un item de la cola"""
        index = self.queueList.row(item)
        if 0 <= index < len(self.queue):
            self.current_index = index
            self.reproducir_actual()
    
    def reproducir_album(self):
        """Reproduce todo el álbum actual"""
        if not self.current_album_songs:
            QMessageBox.warning(self, "Sin álbum", "Selecciona un álbum primero.")
            return
        
        self.queue = [song['StreamUrl'] for song in self.current_album_songs]
        self.queue_info = self.current_album_songs.copy()
        self.current_index = 0
        self.actualizar_lista_cola()
        self.reproducir_actual()
    
    def agregar_todo_album(self):
        """Agrega todas las canciones del álbum actual a la cola"""
        if not self.current_album_songs:
            QMessageBox.warning(self, "Sin álbum", "Selecciona un álbum primero.")
            return
        
        for song in self.current_album_songs:
            self.queue.append(song['StreamUrl'])
            self.queue_info.append(song)
        
        self.actualizar_lista_cola()
        QMessageBox.information(self, "Álbum agregado", 
                              f"Se agregaron {len(self.current_album_songs)} canciones.")
    
    def actualizar_lista_cola(self):
        """Actualiza la lista visual de la cola de reproducción"""
        self.queueList.clear()
        for i, song_info in enumerate(self.queue_info):
            display_text = f"{i+1:02d}. {song_info['Titulo']} ({song_info['Duracion']})"
            if i == self.current_index and self.is_playing:
                display_text = "▶ " + display_text
            item = QListWidgetItem(display_text)
            self.queueList.addItem(item)
        
        self.actualizar_estado_botones()
    
    def actualizar_estado_botones(self):
        """Actualiza el estado habilitado/deshabilitado de los botones"""
        has_queue = len(self.queue) > 0
        has_previous = self.current_index > 0
        has_next = self.current_index < len(self.queue) - 1
        
        self.playButton.setEnabled(has_queue and not self.is_playing)
        self.pauseButton.setEnabled(self.is_playing)
        self.prevButton.setEnabled(has_queue and has_previous)
        self.nextButton.setEnabled(has_queue and has_next)
        self.stopButton.setEnabled(self.is_playing or self.is_paused)
        self.shuffleButton.setEnabled(len(self.queue) > 1)
    
    def limpiar_cola(self):
        """Limpia la cola de reproducción"""
        self.queue.clear()
        self.queue_info.clear()
        self.current_index = -1
        self.detener()
        self.actualizar_lista_cola()
        QMessageBox.information(self, "Cola limpiada", "Cola de reproducción limpiada.")
    
    def aleatorio(self):
        """Reproduce las canciones en orden aleatorio"""
        if len(self.queue) <= 1:
            return
        
        import random
        # Mezclar solo las canciones que quedan por reproducir
        remaining_songs = self.queue[self.current_index + 1:]
        remaining_info = self.queue_info[self.current_index + 1:]
        
        # Crear pares de (url, info) para mezclar juntos
        pairs = list(zip(remaining_songs, remaining_info))
        random.shuffle(pairs)
        
        # Reemplazar las canciones restantes
        self.queue[self.current_index + 1:] = [pair[0] for pair in pairs]
        self.queue_info[self.current_index + 1:] = [pair[1] for pair in pairs]
        
        self.actualizar_lista_cola()
        QMessageBox.information(self, "Aleatorio", "Cola mezclada.")
    
    def on_search_changed(self, text):
        """Filtra la lista de álbumes según el texto de búsqueda"""
        for i in range(self.albumsList.count()):
            item = self.albumsList.item(i)
            album = item.data(Qt.UserRole)
            
            # Buscar en nombre del álbum y artista
            search_text = text.lower()
            album_name = album['Nombre'].lower()
            artist_name = album['Artista'].lower()
            
            if search_text in album_name or search_text in artist_name:
                item.setHidden(False)
            else:
                item.setHidden(True)
    
    def on_error(self, error_msg):
        """Maneja errores del worker thread"""
        self.statusLabel.setText(f"❌ Error: {error_msg}")
        QMessageBox.critical(self, "Error", f"Error: {error_msg}")
    
    def on_volume_changed(self, value):
        """Maneja cambios en el volumen"""
        if self.player:
            self.player.audio_set_volume(value)
    
    def on_balance_changed(self, value):
        """Maneja cambios en el balance"""
        if self.player:
            # Convertir de -100/100 a -1.0/1.0
            balance = value / 100.0
            self.player.audio_set_balance(balance)
    
    def reproducir_actual(self):
        """Reproduce la canción actual de la cola"""
        if not self.queue or self.current_index < 0:
            return
        
        try:
            if self.player:
                # Si está pausado, solo reanudar
                if self.is_paused:
                    self.player.set_pause(0)
                    self.is_playing = True
                    self.is_paused = False
                    self.visualizer.start_animation()
                    self.actualizar_lista_cola()
                    return
                self.player.stop()
            
            media = self.instance.media_new(self.queue[self.current_index])
            self.player.set_media(media)
            self.player.play()
            
            self.is_playing = True
            self.is_paused = False
            
            # Actualizar interfaz
            song_info = self.queue_info[self.current_index]
            self.currentSongLabel.setText(f"{song_info['Titulo']} ({song_info['Duracion']})")
            self.visualizer.start_animation()
            
            # Intentar conectar evento de fin de canción (con manejo de errores)
            try:
                event_manager = self.player.event_manager()
                if event_manager:
                    event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, self.song_ended)
            except Exception as e:
                print(f"Error al conectar evento de fin de canción: {e}")
            
            self.actualizar_lista_cola()
            
        except Exception as e:
            QMessageBox.critical(self, "Error de reproducción", f"Error al reproducir: {str(e)}")
    
    def pausar(self):
        """Pausa la reproducción actual"""
        if self.player and self.is_playing:
            try:
                self.player.pause()
                self.is_playing = False
                self.is_paused = True
                self.visualizer.stop_animation()
                self.actualizar_lista_cola()
            except Exception as e:
                print(f"Error al pausar: {e}")
    
    def siguiente(self):
        """Reproduce la siguiente canción"""
        if self.current_index < len(self.queue) - 1:
            self.current_index += 1
            self.reproducir_actual()
    
    def anterior(self):
        """Reproduce la canción anterior"""
        if self.current_index > 0:
            self.current_index -= 1
            self.reproducir_actual()
    
    def detener(self):
        """Detiene la reproducción"""
        try:
            if self.player:
                # Limpiar eventos antes de detener
                self.limpiar_eventos_vlc()
                self.player.stop()
        except Exception as e:
            print(f"Error al detener: {e}")
        
        self.is_playing = False
        self.is_paused = False
        self.visualizer.stop_animation()
        self.currentSongLabel.setText("Ninguna canción")
        self.timeLabel.setText("00:00 / 00:00")
        self.progressBar.setVisible(False)
        self.actualizar_lista_cola()
    
    def limpiar_eventos_vlc(self):
        """Limpia los eventos de VLC para evitar problemas de memoria"""
        try:
            if self.player:
                event_manager = self.player.event_manager()
                if event_manager:
                    # Detener todos los eventos
                    event_manager.event_detach(vlc.EventType.MediaPlayerEndReached)
        except Exception as e:
            print(f"Error al limpiar eventos VLC: {e}")
    
    def song_ended(self, event):
        """Callback cuando termina una canción"""
        try:
            # Usar QTimer para evitar problemas de threading
            from PyQt5.QtCore import QTimer
            QTimer.singleShot(100, self.siguiente)
        except Exception as e:
            print(f"Error en song_ended: {e}")
    
    def actualizar_tiempo(self):
        """Actualiza el tiempo de reproducción y verifica si la canción terminó"""
        if self.player and self.is_playing:
            try:
                current_time = self.player.get_time()
                total_time = self.player.get_length()
                
                if current_time >= 0 and total_time > 0:
                    current_str = time.strftime('%M:%S', time.gmtime(current_time // 1000))
                    total_str = time.strftime('%M:%S', time.gmtime(total_time // 1000))
                    self.timeLabel.setText(f"{current_str} / {total_str}")
                    
                    # Actualizar barra de progreso
                    progress = int((current_time / total_time) * 100)
                    self.progressBar.setValue(progress)
                    self.progressBar.setVisible(True)
                    
                    # Verificar si la canción terminó (fallback si el evento no funciona)
                    if current_time >= total_time - 1000:  # Si falta menos de 1 segundo
                        self.is_playing = False
                        self.siguiente()
                        
            except Exception as e:
                # Si hay error al obtener el tiempo, la canción probablemente terminó
                if self.is_playing:
                    print(f"Error al obtener tiempo de reproducción: {e}")
                    self.is_playing = False
                    self.siguiente()

def main():
    app = QApplication(sys.argv)
    
    # Configurar estilo de la aplicación
    app.setStyle('Fusion')
    
    # Habilitar íconos del tema
    try:
        from PyQt5.QtGui import QIcon
        # Verificar si los íconos del tema están disponibles
        test_icon = QIcon.fromTheme("media-playback-start")
        if test_icon.isNull():
            print("⚠️  Los íconos del tema no están disponibles. Usando íconos por defecto.")
        else:
            print("✅ Íconos del tema disponibles")
    except Exception as e:
        print(f"⚠️  Error al cargar íconos del tema: {e}")
    
    # Crear y mostrar la ventana principal
    window = ReproductorJellyfinUI()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 