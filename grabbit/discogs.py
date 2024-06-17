import discogs_client
import logging
import time
from typing import List, Dict, Any
from requests.exceptions import RequestException


class Discogs:
    def __init__(
        self,
        api_token: str,
        rate_limit: int = 60,
        max_retries: int = 3,
        log_level: int = logging.INFO,
    ):
        self.client = discogs_client.Client(
            "ExampleApplication/0.1", user_token=api_token
        )
        self.rate_limit = rate_limit
        self.max_retries = max_retries
        logging.basicConfig(level=log_level)

    def search_tracks(self, track: str, artist: str) -> List[Any]:
        """Search for tracks on Discogs by track name and artist."""
        retries = 0
        while retries < self.max_retries:
            try:
                results = self.client.search(track, artist=artist, type="track")
                return results
            except RequestException as e:
                logging.error(f"Request error: {e}")
                retries += 1
                time.sleep(self.rate_limit)
            except Exception as e:
                logging.error(f"Error searching tracks: {e}")
                return []
        return []

    def extract_video_info(self, result: Any) -> List[Dict[str, Any]]:
        """Extract video information from a Discogs result."""
        video_info = []
        if hasattr(result, "videos") and result.videos:
            for video in result.videos:
                video_info.append(
                    {
                        "title": video.title,
                        "uri": video.url,
                        "description": video.description,
                        "duration": video.duration,
                    }
                )
        return video_info

    def extract_related_tracks_and_videos(
        self, results: List[Any]
    ) -> List[Dict[str, Any]]:
        """Extract related tracks and their video information."""
        related_tracks = []
        for result in results:
            track_info = {
                "title": result.title,
                "duration": result.duration,
                "format": result.formats[0]["name"] if result.formats else "",
                "videos": self.extract_video_info(result),
            }
            related_tracks.append(track_info)
        return related_tracks

    def process_track(self, track_info: Dict[str, str]) -> Dict[str, Any]:
        """Process a track to find different versions and related tracks."""
        results = self.search_tracks(track_info["track"], track_info["artist"])
        if not results:
            return {
                "track": track_info["track"],
                "artist": track_info["artist"],
                "versions": [],
                "message": "No results found on Discogs.",
            }
        else:
            track_versions = []
            for result in results:
                version_info = {
                    "title": result.title,
                    "release": result.year,
                    "format": result.formats[0]["name"] if result.formats else "",
                    "videos": self.extract_video_info(result),
                    "related_tracks": self.extract_related_tracks_and_videos(
                        result.tracklist
                    ),
                }
                track_versions.append(version_info)
            return {
                "track": track_info["track"],
                "artist": track_info["artist"],
                "versions": track_versions,
            }
