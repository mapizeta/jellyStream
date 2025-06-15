import requests
from typing import List, Dict, Optional

class JellyfinAPI:
    def __init__(self, jellyfin_url: str, api_key: str, user_id: str):
        """
        Inicializa la conexión con Jellyfin
        
        Args:
            jellyfin_url: URL del servidor Jellyfin (ej: http://192.168.1.144:8096)
            api_key: Clave API de Jellyfin
            user_id: ID del usuario
        """
        self.jellyfin_url = jellyfin_url.rstrip('/')
        self.api_key = api_key
        self.user_id = user_id
        self.session = requests.Session()
        self.session.headers.update({
            'X-Emby-Token': api_key,
            'Content-Type': 'application/json'
        })
    
    def test_connection(self) -> bool:
        """Prueba la conexión con el servidor Jellyfin"""
        try:
            url = f"{self.jellyfin_url}/System/Info"
            params = {"api_key": self.api_key}
            response = self.session.get(url, params=params, timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"Error de conexión: {e}")
            return False
    
    def listar_albumes(self) -> List[Dict]:
        """
        Obtiene la lista de álbumes de música
        
        Returns:
            Lista de diccionarios con información de los álbumes
        """
        url = f"{self.jellyfin_url}/Users/{self.user_id}/Items"
        params = {
            "IncludeItemTypes": "MusicAlbum",
            "Recursive": True,
            "Fields": "PrimaryImageAspectRatio,Overview",
            "SortBy": "SortName",
            "SortOrder": "Ascending",
            "api_key": self.api_key
        }
        
        try:
            response = self.session.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return [
                    {
                        "Nombre": item["Name"],
                        "Id": item["Id"],
                        "Artista": item.get("AlbumArtist", "Desconocido"),
                        "Año": item.get("ProductionYear"),
                        "Imagen": self._get_image_url(item.get("Id")) if item.get("HasPrimaryImage") else None
                    } for item in data.get("Items", [])
                ]
            else:
                print(f"Error al obtener álbumes: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error en listar_albumes: {e}")
            return []
    
    def obtener_canciones_del_album(self, album_id: str) -> List[Dict]:
        """
        Obtiene las canciones de un álbum específico
        
        Args:
            album_id: ID del álbum
            
        Returns:
            Lista de diccionarios con información de las canciones
        """
        url = f"{self.jellyfin_url}/Items"
        params = {
            "ParentId": album_id,
            "IncludeItemTypes": "Audio",
            "Recursive": True,
            "SortBy": "IndexNumber",
            "SortOrder": "Ascending",
            "Fields": "Path,RunTimeTicks",
            "api_key": self.api_key
        }
        
        try:
            response = self.session.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return [
                    {
                        "Titulo": item["Name"],
                        "Id": item["Id"],
                        "Numero": item.get("IndexNumber", 0),
                        "Duracion": self._format_duration(item.get("RunTimeTicks", 0)),
                        "StreamUrl": f"{self.jellyfin_url}/Items/{item['Id']}/Download?api_key={self.api_key}"
                    } for item in data.get("Items", [])
                ]
            else:
                print(f"Error al obtener canciones: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error en obtener_canciones_del_album: {e}")
            return []
    
    def buscar_albumes(self, query: str) -> List[Dict]:
        """
        Busca álbumes por nombre o artista
        
        Args:
            query: Término de búsqueda
            
        Returns:
            Lista de álbumes que coinciden con la búsqueda
        """
        url = f"{self.jellyfin_url}/Users/{self.user_id}/Items"
        params = {
            "IncludeItemTypes": "MusicAlbum",
            "Recursive": True,
            "SearchTerm": query,
            "Fields": "PrimaryImageAspectRatio,Overview",
            "SortBy": "SortName",
            "SortOrder": "Ascending",
            "api_key": self.api_key
        }
        
        try:
            response = self.session.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return [
                    {
                        "Nombre": item["Name"],
                        "Id": item["Id"],
                        "Artista": item.get("AlbumArtist", "Desconocido"),
                        "Año": item.get("ProductionYear"),
                        "Imagen": self._get_image_url(item.get("Id")) if item.get("HasPrimaryImage") else None
                    } for item in data.get("Items", [])
                ]
            else:
                print(f"Error en búsqueda: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error en buscar_albumes: {e}")
            return []
    
    def _get_image_url(self, item_id: str) -> str:
        """Genera la URL para la imagen del álbum"""
        return f"{self.jellyfin_url}/Items/{item_id}/Images/Primary?api_key={self.api_key}"
    
    def _format_duration(self, ticks: int) -> str:
        """Convierte ticks de Jellyfin a formato MM:SS"""
        if not ticks:
            return "00:00"
        seconds = ticks // 10000000  # Jellyfin usa ticks de 100ns
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"


# Configuración por defecto (puedes modificar estos valores)
DEFAULT_CONFIG = {
    "JELLYFIN_URL": "http://192.168.1.144:8096",
    "API_KEY": "a5f1a548ebd144e0b2c63cc309146b9b",
    "USER_ID": "a86f4df1db1b48768fd4f16635bfb280"
} 