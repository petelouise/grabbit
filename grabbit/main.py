import logging
from typing import List, Dict, Any
from discogs import Discogs


def analyze_tracks(
    tracks: List[Dict[str, str]],
    api_token: str,
    rate_limit: int = 60,
    max_retries: int = 3,
    log_level: int = logging.INFO,
) -> List[Dict[str, Any]]:
    discogs_client = Discogs(api_token, rate_limit, max_retries, log_level)

    output_data = []
    for track_info in tracks:
        result = discogs_client.process_track(track_info)
        output_data.append(result)
    return output_data


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Example usage
    api_token = "YOUR_DISCOGS_API_TOKEN"
    tracks = [
        {"track": "Fancy", "artist": "Reba McEntire"},
        {"track": "Shape of You", "artist": "Ed Sheeran"},
    ]

    results = analyze_tracks(tracks, api_token)
    for result in results:
        print(result)
