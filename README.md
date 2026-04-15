# 🎵 Music Recommender Simulation

## Project Summary

**TasteAlchemy 1.0** is a content-based music recommender that matches user preferences (genre, mood, energy) against a catalog of 18 songs to surface personalized recommendations. The system uses weighted scoring—assigning 1.5 points for genre match, 1.0 point for mood match, and up to 1.0 point for energy similarity—then ranks songs by total score and returns the top 5.

This project demonstrates how simple weighting schemes can drive recommendation behavior. By testing profiles with aligned preferences (rock + intense + high-energy), conflicting preferences (metal + melancholic + high-energy), and edge cases (non-existent genres), the system reveals both the strengths of transparent scoring and the biases it introduces—particularly how heavy genre weighting creates "filter bubbles" that lock users into narrow recommendation patterns.


---

## How The System Works

Services like Spotify and YouTube Music use recommendation systems that analyze billions of data points, listening history, skips, playlist patterns, and audio features to predict what each user wants to hear next. They combine multiple techniques, including collaborative filtering (finding users with similar taste) and content-based filtering (matching song attributes like tempo, energy, and mood to a listener's preferences). This simplified version focuses on the content-based approach: it scores each song in a small catalog by comparing its genre, mood, and energy level against a user's taste profile, then ranks the results to surface the best matches. The goal is to make the core logic of a real recommender visible and easy to experiment with, without the complexity of large-scale data pipelines or machine learning models.


- **Song features:** Each `Song` carries two categorical attributes (`genre`, `mood`) and four numeric attributes (`energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness`), plus metadata (`id`, `title`, `artist`).
- **UserProfile:** Stores the user's `favorite_genres`, `favorite_moods`, `target_energy`, `target_valence`, `target_tempo_bpm`, and `target_danceability`. These six fields define the taste profile that songs are scored against.
- **Scoring rule:** The recommender compares each song to the user profile using three features: genre match (+1.5 pts), mood match (+1.0 pt), and energy similarity (up to +1.0 pt via `1 - abs(song_energy - target_energy)`). The max possible score is 3.5. We use 1.5/1.0 instead of the more common 2.0/1.0 split because a 2.0 genre weight lets genre alone tie or beat mood + perfect energy combined (1.0 + 1.0 = 2.0), making energy scoring irrelevant. At 1.5, genre remains the single strongest signal, but mood + energy (up to 2.0) can outrank a genre-only match, so numeric proximity actually influences the final ranking.
- **Ranking rule:** All songs in the catalog are scored, sorted by descending score, and the top *k* results are returned as recommendations.

![alt text](image.png)
---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

**Test 1: Aligned Preferences (Deep Intense Rock)**  
When all three scoring factors align (rock genre, intense mood, 0.9 energy), the top results are clean and intuitive. *Storm Runner* (rock, intense, 0.91 energy) and *Gym Hero* (pop, intense, 0.93 energy) both score well, confirming that energy matching works as the secondary priority when mood aligns.

**Test 2: Contradicted Preferences (Metal + Melancholic)**  
The system struggles here because metal songs are high-energy (0.95) but NOT melancholic. There's no genre-matched song that satisfies both mood and energy, so the system forces a compromise: either recommend melancholic songs (classical, lofi) that don't match the metal genre, or recommend high-energy metal that doesn't match the melancholic mood. This exposes that the system can't detect or communicate preference conflicts.

**Test 3: Non-Existent Genre (Techno + Ethereal)**  
When both genre and mood have zero matches in the dataset, the system falls back entirely to energy scoring. Top results become whatever high-energy songs exist (*Neon Pulse*, *Iron Requiem*), regardless of genre coherence. This shows the system degrades ungracefully—it should alert the user that their preferences don't exist in the catalog.

**Test 4: Opposite Energy Ranges (Chill Lofi vs. High-Energy Pop)**  
The same song (*Storm Runner*, 0.91 energy) ranks at the bottom of lofi recommendations (wanting 0.3 energy) but at the top of rock recommendations (wanting 0.9 energy). This confirms that energy similarity is working correctly and driving meaningful differentiation between user types.

---

## Limitations and Risks

**Genre filter bubbles**: With genre weighted at 1.5/3.5 (43%), songs from non-preferred genres almost never compete even when they match mood or energy perfectly. A user seeking happy songs will score reggae lower than pop, regardless of which better matches their actual taste.

**Dataset imbalance**: Pop and lofi have multiple entries while metal, jazz, and classical each have only one. Users seeking niche genres can't build coherent recommendations—the system becomes useless for them.

**Unused features**: The dataset includes `tempo_bpm` and `valence` but they're never scored. Tempo is especially problematic since it's expected from a music recommender but does nothing.

**No contradiction detection**: The system blindly ranks contradictory preferences (high energy + melancholic mood) instead of warning the user or suggesting alternatives.

**Tiny catalog**: With 18 songs, the recommender is primarily an educational tool. Real Spotify, Apple Music, and YouTube Music systems work on millions of songs and use collaborative filtering, listening history, and neural networks to capture taste complexity that binary genre/mood tags cannot.

See the [Model Card](model_card.md) for deeper analysis.

---

## Key Learnings

**How recommenders turn data into predictions**: TasteAlchemy demonstrates that a recommender is essentially a scoring function that maps user preferences and item attributes to a comparable score. The magic isn't in complexity—it's in choosing which features to weight and how heavily. A change from 1.5 to 2.0 on genre weight doesn't sound like much, but it fundamentally shifts what songs rank highest. Real recommenders do this at scale with hundreds of features (not just 3), but the core principle is identical: assign points, rank, return top results.

**Where bias hides**: Bias in recommenders is often invisible because it's baked into weighting decisions. The 1.5x genre weight in TasteAlchemy looks "neutral"—it's just a number—but it creates massive filter bubbles and disadvantages underrepresented genres. A user seeking metal music sees worse and worse recommendations because the system gives them fewer options in their category. Meanwhile, pop and lofi users get great recommendations because they have diversity in the dataset. This isn't intentional unfairness, but it IS structural unfairness. Real recommenders (Spotify, YouTube) amplify this at scale: they over-recommend mainstream content, lock users into "algorithmic serendipity" controlled by engineers, and make niche artists harder to discover. The numbers look objective, but they encode human choices about what matters—and those choices have real consequences.


---

