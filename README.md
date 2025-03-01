# Entertainment AI Agent
This AI agent is designed to provide personalized recommendations for movies, music, books, and games based on user preferences and current trends. It uses a modular design with classes for managing entertainment items, user profiles, an entertainment database, and a recommendation engine.

## Features
-   **Entertainment Item Management:**
    -   Base class `EntertainmentItem` for common attributes like ID, title, genre, year, and rating.
    -   Specific classes for `Movie`, `Music`, `Book`, and `Game` with additional attributes relevant to each type.
-   **User Profile Management:**
    -   `UserProfile` class to store user preferences (genres, actors, directors, artists, authors, developers, platforms, years, ratings) and history of consumed items.
    -   Methods to add preferences and track user history.
-   **Entertainment Database:**
    -   `EntertainmentDatabase` class to manage collections of movies, music, books, and games.
    -   Methods to add, retrieve, save, and load entertainment items from a JSON file.
    -   Includes sample data for demonstration purposes.
-   **Recommendation Engine:**
    -   `RecommendationEngine` class to generate personalized recommendations based on user preferences.
    -   `calculate_match_score` method to determine how well an item matches a user's preferences, taking into account various factors like genre, year, actors, directors, artists, authors, developers, and platforms.
    -   Considers user history to avoid recommending items already consumed.

## Getting Started
### Prerequisites
-   Python 3.6+

### Installation
1.  Clone the repository:

    ```
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  (Optional) Create a virtual environment:

    ```
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

### Usage

1.  **Import the necessary classes:**

    ```
    from entertainment_ai_agent import EntertainmentDatabase, UserProfile, RecommendationEngine
    ```

2.  **Initialize the entertainment database:**

    ```
    db = EntertainmentDatabase()
    # Optionally load data from a JSON file
    # db.load_from_file("entertainment_db.json")
    ```

3.  **Create a user profile:**

    ```
    user = UserProfile("user123", "Alice")
    ```

4.  **Add user preferences:**

    ```
    user.add_preference("movie", "genres", "Action")
    user.add_preference("movie", "actors", "Robert Downey Jr.")
    user.add_preference("music", "artists", "Queen")
    ```

5.  **Initialize the recommendation engine:**

    ```
    engine = RecommendationEngine(db)
    ```

6.  **Generate recommendations:**

    ```
    # Example: Get movie recommendations
    movies = db.get_movies()
    movie_scores = {movie.item_id: engine.calculate_match_score(movie, user, "movie") for movie in movies}
    sorted_movies = sorted(movie_scores.items(), key=lambda x: x[1], reverse=True)
    
    print("Recommended Movies:")
    for movie_id, score in sorted_movies[:5]:  # Top 5 movies
        movie = db.get_movie_by_id(movie_id)
        print(f"- {movie.title} (Score: {score:.2f})")
    ```

7.  **Add items to user history:**

    ```
    user.add_to_history("movie", "m5")  # User watched Avengers: Endgame
    ```

8.  **Save the database:**

    ```
    db.save_to_file("entertainment_db.json")
    ```

## Class Details

### EntertainmentItem

-   **Attributes:**
    -   `item_id` (str): Unique identifier for the item.
    -   `title` (str): Title of the item.
    -   `genre` (List\[str]): List of genres.
    -   `year` (int): Year of release.
    -   `rating` (float): Rating of the item.
-   **Methods:**
    -   `to_dict()`: Returns a dictionary representation of the item.

### Movie, Music, Book, Game

-   Inherit from `EntertainmentItem`.
-   Include additional attributes specific to their media type.
-   Override `to_dict()` to include these additional attributes.

### UserProfile

-   **Attributes:**
    -   `user_id` (str): Unique identifier for the user.
    -   `name` (str): User's name.
    -   `preferences` (Dict): Dictionary storing user preferences for each media type (movie, music, book, game).
    -   `history` (Dict): Dictionary storing the user's history of consumed items for each media type.
-   **Methods:**
    -   `add_preference(media_type: str, category: str, value: Union[str, int, float])`: Adds a user preference.
    -   `add_to_history(media_type: str, item_id: str)`: Adds an item to the user's history.
    -   `to_dict()`: Returns a dictionary representation of the user profile.
    -   `from_dict(data: Dict)`: Creates a `UserProfile` object from a dictionary.

### EntertainmentDatabase
-   **Attributes:**
    -   `movies` (Dict\[str, Movie]): Dictionary of movies.
    -   `music` (Dict\[str, Music]): Dictionary of music.
    -   `books` (Dict\[str, Book]): Dictionary of books.
    -   `games` (Dict\[str, Game]): Dictionary of games.
-   **Methods:**
    -   `add_movie(movie: Movie)`: Adds a movie to the database.
    -   `add_music(music: Music)`: Adds a music item to the database.
    -   `add_book(book: Book)`: Adds a book to the database.
    -   `add_game(game: Game)`: Adds a game to the database.
    -   `get_movies() -> List[Movie]`: Returns a list of all movies.
    -   `get_music() -> List[Music]`: Returns a list of all music.
    -   `get_books() -> List[Book]`: Returns a list of all books.
    -   `get_games() -> List[Game]`: Returns a list of all games.
    -   `get_movie_by_id(movie_id: str) -> Optional[Movie]`: Returns a movie by its ID.
    -   `get_music_by_id(music_id: str) -> Optional[Music]`: Returns a music item by its ID.
    -   `get_book_by_id(book_id: str) -> Optional[Book]`: Returns a book by its ID.
    -   `get_game_by_id(game_id: str) -> Optional[Game]`: Returns a game by its ID.
    -   `save_to_file(filename: str = "entertainment_db.json")`: Saves the database to a JSON file.
    -   `load_from_file(filename: str = "entertainment_db.json")`: Loads the database from a JSON file.

### RecommendationEngine
-   **Attributes:**
    -   `db` (`EntertainmentDatabase`): The entertainment database to use for recommendations.
-   **Methods:**
    -   `calculate_match_score(item: EntertainmentItem, user: UserProfile, media_type: str) -> float`: Calculates a match score between an item and a user based on their preferences.

## Contributing
- Contributions are welcome! Please submit a pull request with your changes.

## License
[Choose a license, e.g., MIT License]
