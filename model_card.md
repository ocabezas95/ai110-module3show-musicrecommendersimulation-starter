# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**TasteAlchemy 1.0**  

---

## 2. Intended Use  

TasteAlchemy generates personalized song recommendations by matching user preferences in genre, mood, and energy level. It's designed for exploration of how weighted scoring systems work in recommendations, rather than production use. The system assumes users can clearly specify their genre taste and emotional mood, which limits real-world applicability but makes the scoring logic transparent and testable.  

---

## 3. How the Model Works  

The recommender scores each song on a scale of 0 to 3.5 points based on three factors:

1. **Genre match** (1.5 points): Does the song's genre match what the user asked for? If yes, +1.5 points. If no, zero points—this is the heaviest weight, so genre choice matters most.

2. **Mood match** (1.0 point): Does the song's mood (happy, chill, intense, etc.) match the user's preference? If yes, +1.0 point. If no, zero points.

3. **Energy similarity** (up to 1.0 point): How close is the song's energy level to what the user wants? If it's a perfect match (user wants 0.8 energy, song is 0.8), that's +1.0 point. If it's off by 0.3, the song gets partial credit—maybe +0.7 points.

The top 5 songs with the highest total scores are recommended. Because genre is weighted so heavily, popular genres like pop and lofi tend to dominate the results, even when other genres might match the user's mood better.

---

## 4. Data  

The dataset contains **18 songs** across 15 different genres. Genres include pop, lofi, rock, ambient, jazz, synthwave, indie pop, metal, reggae, classical, R&B, electronic, country, hip-hop, and latin. Moods range from happy and chill to intense, melancholic, and energetic. The energy levels span the full 0.0–1.0 range, from slow classical pieces (0.30) to high-intensity metal songs (0.95).

The dataset is balanced enough for classroom testing but has real limitations: pop and lofi have multiple entries while metal, jazz, and classical each have only one. This artificial imbalance exposes a key weakness of weighted scoring—users seeking niche genres can't get good recommendations because there's insufficient variety in those categories. No songs were added or removed from the original dataset.  

---

## 5. Strengths  

TasteAlchemy works best for users with **aligned preferences**—when their genre choice, mood, and energy level naturally go together. For example, the Deep Intense Rock profile (rock + intense + 0.9 energy) gets clean, intuitive recommendations because all three scoring factors point to the same songs. The system is also effective for users in the **mainstream genres** like pop and lofi that have multiple entries in the dataset, since variety ensures good recommendations. 

The energy scoring is the system's strongest feature: because it's a continuous scale (0.0–1.0) rather than binary like genre and mood, it captures fine-grained preferences. A user who wants exactly 0.3 energy (chill) gets meaningfully different results than one wanting 0.8 energy (upbeat), which matches real musical taste variation. The recommender correctly surfaces that these two profiles need completely different songs, which shows the energy component works as intended.  

---

## 6. Limitations and Bias 

Genre weight creates strong filter bubbles that lock users into narrow recommendation patterns. With genre accounting for 43% of the maximum score, songs from non-preferred genres rarely compete even when they match user mood or energy preferences perfectly. For example, a user who loves "happy" mood songs will score a genre-mismatched reggae track much lower than a genre-matched pop song, regardless of which better suits their actual preferences. This overweighting of categorical matching over contextual fit means the system trains users to expect genre-locked recommendations rather than discovering serendipitous cross-genre hits. Additionally, rare genres (metal, jazz, classical) with only one entry in the dataset are structurally disadvantaged users seeking those genres cannot build coherent recommendations and instead see LoFi/Pop dominate by default.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected.

### Test Profiles Used

I tested four distinct user profiles to verify the scoring logic:
- **Starter Profile**: Pop + Happy + 0.8 energy (normal case)
- **Chill Lofi**: Lofi + Chill + 0.3 energy (relaxed listening)
- **Deep Intense Rock**: Rock + Intense + 0.9 energy (high-energy rock)
- **Contradicted User**: Metal + Melancholic + 0.95 energy (conflicting preferences)
- **Genre Ghost**: Techno (non-existent) + Ethereal (non-existent) + 0.8 energy (edge case)

### Comparison Notes

**Starter Profile vs. Chill Lofi**: When the user switches from happy pop hits to relaxing lofi beats, the energy preference drops from 0.8 to 0.3—so songs like *Gym Hero* (0.93 energy) that dominated the pop list suddenly disappear, replaced by *Library Rain* and *Midnight Coding*, which are slow enough to match what the user actually wants to listen to.

**Deep Intense Rock vs. Chill Lofi**: These two profiles are almost complete opposites: deep intense rock wants high energy songs (0.9) while chill lofi wants low-energy songs (0.3), so *Storm Runner* jumps from the bottom of the lofi list to the very top of the rock list—same song, but energy matching flips it from poor fit to perfect fit.

**Contradicted User vs. Deep Intense Rock**: The contradicted user asks for metal + melancholic mood + 0.95 energy but metal and intense rock songs have high energy but NOT melancholic vibes, forcing the system to compromise; meanwhile, deep intense rock aligns all preferences (rock genre, intense mood, high energy), so it gets clean recommendations without trade-offs.

**Starter Profile vs. Genre Ghost**: When the user requests a "techno" genre that doesn't exist in the dataset plus a made-up "ethereal" mood, the recommender can't use genre or mood scoring at all and falls back entirely to energy matching—so the top results become whatever high-energy songs exist (like *Neon Pulse* and *Iron Requiem*) rather than genre-coherent hits like *Sunrise City*.

---

## 8. Future Work  

**Expand underrepresented genres**: Add more metal, jazz, and classical songs so users seeking niche genres aren't limited by dataset imbalance. This directly addresses the "rare genre disadvantage" exposed in testing.

**Use the unused tempo feature**: The dataset includes `tempo_bpm` but it's never scored. Adding tempo matching (similar to energy scoring) would give users finer control over tempo preferences and help distinguish between songs with similar energy.

**Detect and handle contradictions**: When a user asks for conflicting preferences (high energy + melancholic mood), the system could warn the user or suggest they adjust their preferences rather than forcing poor compromises. This would make recommendations more transparent.

**Inject diversity into results**: Instead of always returning the top 5 scores, occasionally include slightly lower-scoring songs from different genres to break filter bubbles and enable cross-genre discovery—the opposite of what currently happens.

**Let users adjust weights**: Allow power users to set their own weights (e.g., "energy matters twice as much as mood to me") so the system is less one-size-fits-all.  

---


