import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# Constants for the scoring weights (out of 3.5 total)
GENRE_WEIGHT = 1.5
MOOD_WEIGHT = 1.0
ENERGY_WEIGHT = 1.0


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genres: List[str]
    favorite_moods: List[str]
    target_energy: float
    target_valence: float
    target_tempo_bpm: float
    target_danceability: float


def score_song(user: UserProfile, song: Song) -> float:
    """
    Score a song against a user profile using weighted hybrid scoring.

    - Genre match: +1.5 points (binary)
    - Mood match:  +1.0 point  (binary)
    - Energy:      up to +1.0  (inverse distance)

    Returns a score between 0.0 and 3.5.
    """
    score = 0.0

    # Categorical scoring
    score += GENRE_WEIGHT if song.genre in user.favorite_genres else 0
    score += MOOD_WEIGHT if song.mood in user.favorite_moods else 0

    # Numerical scoring (energy is already on 0-1 scale)
    score += ENERGY_WEIGHT * (1.0 - abs(song.energy - user.target_energy))

    return round(score, 2)


def explain_score(user: UserProfile, song: Song) -> str:
    """Build a human-readable explanation of why a song was recommended."""
    reasons = []

    if song.genre in user.favorite_genres:
        reasons.append(f"genre is {song.genre} (+{GENRE_WEIGHT})")
    if song.mood in user.favorite_moods:
        reasons.append(f"mood is {song.mood} (+{MOOD_WEIGHT})")

    energy_pts = round(ENERGY_WEIGHT * (1.0 - abs(song.energy - user.target_energy)), 2)
    reasons.append(f"energy similarity (+{energy_pts}/{ENERGY_WEIGHT})")

    if not reasons:
        return "No strong matches, but still in your top results."

    return "Matched because: " + ", ".join(reasons)


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored = [(song, score_song(user, song)) for song in self.songs]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        total = score_song(user, song)
        explanation = explain_score(user, song)
        return f"Score: {total}/3.5. {explanation}"


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row.get("id"):
                continue
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py

    Accepts a simple prefs dict (from main.py) and a list of song dicts.
    Returns list of (song_dict, score, explanation) tuples sorted by score descending.
    """
    # Build a UserProfile from the prefs dict, using sensible defaults
    user = UserProfile(
        favorite_genres=[user_prefs["genre"]] if "genre" in user_prefs else [],
        favorite_moods=[user_prefs["mood"]] if "mood" in user_prefs else [],
        target_energy=user_prefs.get("energy", 0.5),
        target_valence=user_prefs.get("valence", 0.5),
        target_tempo_bpm=user_prefs.get("tempo_bpm", 110),
        target_danceability=user_prefs.get("danceability", 0.5),
    )

    results = []
    for s in songs:
        song_obj = Song(
            id=s["id"], title=s["title"], artist=s["artist"],
            genre=s["genre"], mood=s["mood"], energy=s["energy"],
            tempo_bpm=s["tempo_bpm"], valence=s["valence"],
            danceability=s["danceability"], acousticness=s["acousticness"],
        )
        sc = score_song(user, song_obj)
        explanation = explain_score(user, song_obj)
        results.append((s, sc, explanation))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:k]
