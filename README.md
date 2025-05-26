# 🎬 Movie Filter Tool

A Python script to filter IMDb rating data using flexible command-line arguments. You can filter movies by votes, rating, genre, runtime, type, and more. The script also supports saving and automatically opening filtered results in a spreadsheet.

---

## 📦 Requirements

- Python 3.7+
- pandas

Install required packages:
```bash
pip install pandas
```

---

## 🚀 Usage Example

```bash
python movie_filter.py --data_path ./data.csv --min_votes 50000 --min_rating 7.5 --include_genres "Action,Thriller" --exclude_genres Animation --num_movies 10
```

---

## 📄 Arguments

| Argument           | Type    | Default           | Description |
|--------------------|---------|-------------------|-------------|
| `--data_path`       | `str`   | `./data.csv`       | Path to the input IMDb ratings data CSV or TSV file. |
| `--min_votes`       | `int`   | `100000`           | Minimum number of votes a movie must have to be included. |
| `--max_votes`       | `int`   | `-1` (no max)       | Maximum number of votes allowed. |
| `--min_rating`      | `float` | `0.0`              | Minimum IMDb rating. |
| `--max_rating`      | `float` | `10.0`             | Maximum IMDb rating. |
| `--title_types`     | `str`   | `"movie, tvMovie"` | Comma-separated list of title types to include. Use `"all"` to include everything.<br>Available types: `movie`, `short`, `tvEpisode`, `tvMiniSeries`, `tvMovie`, `tvSeries`, `tvShort`, `tvSpecial`, `video`, `videoGame`. |
| `--include_genres`  | `str`   | _None_             | Only include movies that match these genres (comma-separated). |
| `--exclude_genres`  | `str`   | _None_             | Exclude movies that match these genres (comma-separated). |
| `--min_runtime`     | `str`   | _None_             | Minimum runtime in minutes (e.g., `'30'`). |
| `--max_runtime`     | `str`   | _None_             | Maximum runtime in minutes (e.g., `'120'`). |
| `--min_year`        | `int`   | _None_             | Only include movies from this year or later. |
| `--num_movies`      | `int`   | `20`               | Number of movies to display after filtering. |
| `--save_path`       | `str`   | _None_             | Save filtered results to a file (e.g., `filtered.csv`). |
| `--open`            | _flag_  | _False_            | If included, automatically opens the saved file in your spreadsheet application (Excel, Numbers, etc.). |

---

## ✅ Example Commands

Filter highly-rated action films:
```bash
python movie_filter.py --min_rating 8 --include_genres Action
```

Filter short films from 2020 onward and save the result:
```bash
python movie_filter.py --title_types short --min_year 2020 --save_path short_films.csv --open
```

Show top 5 horror films under 90 minutes:
```bash
python movie_filter.py --include_genres Horror --max_runtime 90 --num_movies 5
```

---

## 📂 Output

If `--save_path` is provided:
- The filtered dataset is saved to the specified path.
- If `--open` is used, the saved file will be opened automatically.

---

## 📬 License

SAW-CON-2 license, feel free to edit.
