import argparse
import pandas as pd
import os
import platform
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser(description="Filter IMDb ratings based on number of votes.")
parser.add_argument("--data_path", type=str, default="./data.csv", help="Path to the IMDb ratings data csv or tsv file")
parser.add_argument("--min_votes", type=int, default=100000, help="Minimum number of votes to filter ratings")
parser.add_argument("--max_votes", type=int, default=-1, help="Maximum number of votes to filter ratings")
parser.add_argument("--min_rating", type=float, default=0.0, help="Minimum rating to filter")
parser.add_argument("--max_rating", type=float, default=10.0, help="Maximum rating to filter")
parser.add_argument("--title_types", type=str, default="movie, tvMovie", help=r"Type of title to filter ('all', 'movie', 'short', 'tvEpisode', 'tvMiniSeries', 'tvMovie', 'tvSeries', 'tvShort', 'tvSpecial', 'video', 'videoGame')")
parser.add_argument("--include_genres", type=str, 
                    help="Genres to filter. Omit if you want all. (comma-separated: 'Documentary', 'Adventure', 'Game-Show', 'Short', 'Action', 'Film-Noir', 'Music', 'Sport', 'Talk-Show', 'Western', 'War', 'Sci-Fi', 'Fantasy', 'Romance', 'News', 'Family', 'Reality-TV', 'Drama', 'Animation', 'Comedy', 'History', 'Mystery', 'Musical', 'Thriller', 'Crime', 'Adult', 'Horror', 'Biography')")
parser.add_argument("--exclude_genres", type=str, 
                    help="Genres to filter. Omit if you want all. (comma-separated: 'Documentary', 'Adventure', 'Game-Show', 'Short', 'Action', 'Film-Noir', 'Music', 'Sport', 'Talk-Show', 'Western', 'War', 'Sci-Fi', 'Fantasy', 'Romance', 'News', 'Family', 'Reality-TV', 'Drama', 'Animation', 'Comedy', 'History', 'Mystery', 'Musical', 'Thriller', 'Crime', 'Adult', 'Horror', 'Biography')")
parser.add_argument("--max_runtime", type=str, help="Maximum runtime to filter in minutes. (e.g., '90')")
parser.add_argument("--min_runtime", type=str, help="Minimum runtime to filter in minutes. (e.g., '30')")
parser.add_argument("--min_year", type=int, help="Earliest year to filter from (e.g., '2000')")
parser.add_argument("--num_movies", type=int, help="Number of movies to display after filtering. Default is 20.", default=20)
parser.add_argument("--save_path", type=str, help="Save the filtered data to a CSV file. Provide the file name (e.g., 'data_filtered.csv').")
parser.add_argument("--open", action="store_true", help="Automatically open the filtered data in a spreadsheet application.")
args = parser.parse_args()

if args.data_path.endswith(".tsv"):
    data = pd.read_csv(args.data_path, sep="\t")
elif args.data_path.endswith(".csv"):
    data = pd.read_csv(args.data_path)
else:
    raise ValueError("Unsupported file format. Please provide a .csv or .tsv file.")

data = data[data["numVotes"] >= args.min_votes]
if args.max_votes > -1:
    data = data[data["numVotes"] <= args.max_votes]
data = data[(data["averageRating"] >= args.min_rating) & (data["averageRating"] <= args.max_rating)]

title_types = args.title_types.replace(" ", "")
title_types = title_types.split(",")
if "all" in title_types:
    title_types = ["movie", "short", "tvEpisode", "tvMiniSeries", "tvMovie", "tvSeries", "tvShort", "tvSpecial", "video", "videoGame"]
data = data[data["titleType"].isin(title_types)]

if args.include_genres is not None:
    genres = args.include_genres.replace(" ", "")
    genres = genres.split(",")
    for genre in genres:
        data = data[data["genres"].str.contains(genre, na=False)]

if args.exclude_genres is not None:
    genres = args.exclude_genres.replace(" ", "")
    genres = genres.split(",")
    for genre in genres:
        data = data[~data["genres"].str.contains(genre, na=False)]

data["runtimeMinutes"] = pd.to_numeric(data["runtimeMinutes"], errors='coerce')

if args.max_runtime is not None:
    data = data[data["runtimeMinutes"] <= int(args.max_runtime)]

data = data[(data["runtimeMinutes"] >= int(args.min_runtime))] if args.min_runtime else data

data["startYear"] = pd.to_numeric(data["startYear"], errors='coerce')

data = data[data["startYear"] >= int(args.min_year)] if args.min_year else data

data.sort_values(by="averageRating", ascending=False, inplace=True)

print(f"\n🎬 {len(data)} movies found after filtering.🎬\n")
print(f"\nShowing the top {args.num_movies}:\n")
#---------------#
print(f"{'Title':<50} {'Rating':<6} {'Genres':<30} {'Runtime':<8} {'Year':<6}")
print("-" * 110)

for _, row in data[["primaryTitle", "averageRating", "genres", "runtimeMinutes", "startYear", "tconst"]].head(args.num_movies).iterrows():
    title = str(row['primaryTitle'])[:47] + '...' if len(str(row['primaryTitle'])) > 50 else str(row['primaryTitle'])
    genres = str(row['genres'])[:27] + '...' if len(str(row['genres'])) > 30 else str(row['genres'])
    imdb_url = f"https://www.imdb.com/title/{row['tconst']}"
    print(f"{title:<50} {row['averageRating']:<6.1f} {genres:<30} {int(row['runtimeMinutes']):<8} {int(row['startYear'])}")
    print(f"    🔗 IMDb: {imdb_url}\n")

if args.save_path is not None:
    assert args.save_path.endswith('.csv'), "Save path must end with .csv"
    assert Path(args.save_path).resolve() != Path(args.data_path).resolve(), "Cannot overwrite the original data file. Please provide a different save path."
    data["IMDb Link"] = "https://www.imdb.com/title/" + data["tconst"]
    data.to_csv(args.save_path, index=False)
    print(f"\nFiltered data saved to {args.save_path}.")
    print(args.open)
    if args.open:
        if platform.system() == "Windows":
            os.startfile(args.save_path)
        elif platform.system() == "Darwin":
            subprocess.run(["open", args.save_path])
        elif platform.system() == "Linux":
            subprocess.run(["xdg-open", args.save_path])
