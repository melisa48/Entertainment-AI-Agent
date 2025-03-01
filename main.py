# Entertainment AI Agent
# This AI agent recommends movies, music, books, and games based on user preferences and current trends

import json
import random
from datetime import datetime
from typing import Dict, List, Optional, Union

class EntertainmentItem:
    """Base class for all entertainment items."""
    def __init__(self, item_id: str, title: str, genre: List[str], year: int, rating: float):
        self.item_id = item_id
        self.title = title
        self.genre = genre
        self.year = year
        self.rating = rating
    
    def to_dict(self) -> Dict:
        return {
            "id": self.item_id,
            "title": self.title,
            "genre": self.genre,
            "year": self.year,
            "rating": self.rating
        }

class Movie(EntertainmentItem):
    """Class representing a movie."""
    def __init__(self, item_id: str, title: str, genre: List[str], year: int, rating: float, 
                 director: str, actors: List[str], duration: int):
        super().__init__(item_id, title, genre, year, rating)
        self.director = director
        self.actors = actors
        self.duration = duration  # in minutes
    
    def to_dict(self) -> Dict:
        movie_dict = super().to_dict()
        movie_dict.update({
            "director": self.director,
            "actors": self.actors,
            "duration": self.duration,
            "type": "movie"
        })
        return movie_dict

class Music(EntertainmentItem):
    """Class representing a music album or track."""
    def __init__(self, item_id: str, title: str, genre: List[str], year: int, rating: float,
                 artist: str, album: Optional[str] = None, duration: Optional[int] = None):
        super().__init__(item_id, title, genre, year, rating)
        self.artist = artist
        self.album = album
        self.duration = duration  # in seconds
    
    def to_dict(self) -> Dict:
        music_dict = super().to_dict()
        music_dict.update({
            "artist": self.artist,
            "album": self.album,
            "duration": self.duration,
            "type": "music"
        })
        return music_dict

class Book(EntertainmentItem):
    """Class representing a book."""
    def __init__(self, item_id: str, title: str, genre: List[str], year: int, rating: float,
                 author: str, pages: int, publisher: str):
        super().__init__(item_id, title, genre, year, rating)
        self.author = author
        self.pages = pages
        self.publisher = publisher
    
    def to_dict(self) -> Dict:
        book_dict = super().to_dict()
        book_dict.update({
            "author": self.author,
            "pages": self.pages,
            "publisher": self.publisher,
            "type": "book"
        })
        return book_dict

class Game(EntertainmentItem):
    """Class representing a video game."""
    def __init__(self, item_id: str, title: str, genre: List[str], year: int, rating: float,
                 developer: str, platforms: List[str], multiplayer: bool):
        super().__init__(item_id, title, genre, year, rating)
        self.developer = developer
        self.platforms = platforms
        self.multiplayer = multiplayer
    
    def to_dict(self) -> Dict:
        game_dict = super().to_dict()
        game_dict.update({
            "developer": self.developer,
            "platforms": self.platforms,
            "multiplayer": self.multiplayer,
            "type": "game"
        })
        return game_dict

class UserProfile:
    """Class to store and manage user preferences."""
    def __init__(self, user_id: str, name: str):
        self.user_id = user_id
        self.name = name
        self.preferences = {
            "movie": {"genres": [], "actors": [], "directors": [], "years": [], "ratings": []},
            "music": {"genres": [], "artists": [], "years": [], "ratings": []},
            "book": {"genres": [], "authors": [], "years": [], "ratings": []},
            "game": {"genres": [], "developers": [], "platforms": [], "years": [], "ratings": []}
        }
        self.history = {
            "movie": [],
            "music": [],
            "book": [],
            "game": []
        }
    
    def add_preference(self, media_type: str, category: str, value: Union[str, int, float]):
        """Add a user preference."""
        if media_type in self.preferences and category in self.preferences[media_type]:
            if value not in self.preferences[media_type][category]:
                self.preferences[media_type][category].append(value)
    
    def add_to_history(self, media_type: str, item_id: str):
        """Add an item to user's history."""
        if media_type in self.history and item_id not in self.history[media_type]:
            self.history[media_type].append(item_id)
    
    def to_dict(self) -> Dict:
        return {
            "user_id": self.user_id,
            "name": self.name,
            "preferences": self.preferences,
            "history": self.history
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'UserProfile':
        user = cls(data["user_id"], data["name"])
        user.preferences = data["preferences"]
        user.history = data["history"]
        return user

class EntertainmentDatabase:
    """Class to manage the entertainment items database."""
    def __init__(self):
        self.movies = {}
        self.music = {}
        self.books = {}
        self.games = {}
        
        # Initialize with sample data
        self._load_sample_data()
    
    def _load_sample_data(self):
        """Load sample entertainment data."""
        # Sample Movies
        self.add_movie(Movie("m1", "The Shawshank Redemption", ["Drama"], 1994, 9.3, 
                            "Frank Darabont", ["Tim Robbins", "Morgan Freeman"], 142))
        self.add_movie(Movie("m2", "The Godfather", ["Crime", "Drama"], 1972, 9.2, 
                            "Francis Ford Coppola", ["Marlon Brando", "Al Pacino"], 175))
        self.add_movie(Movie("m3", "Inception", ["Action", "Sci-Fi"], 2010, 8.8, 
                            "Christopher Nolan", ["Leonardo DiCaprio", "Joseph Gordon-Levitt"], 148))
        self.add_movie(Movie("m4", "Parasite", ["Drama", "Thriller"], 2019, 8.6, 
                            "Bong Joon Ho", ["Song Kang-ho", "Lee Sun-kyun"], 132))
        self.add_movie(Movie("m5", "Avengers: Endgame", ["Action", "Adventure", "Sci-Fi"], 2019, 8.4, 
                            "Anthony Russo, Joe Russo", ["Robert Downey Jr.", "Chris Evans"], 181))
        
        # Sample Music
        self.add_music(Music("mu1", "Bohemian Rhapsody", ["Rock"], 1975, 9.5, 
                            "Queen", "A Night at the Opera", 354))
        self.add_music(Music("mu2", "Thriller", ["Pop", "R&B"], 1982, 9.4, 
                            "Michael Jackson", "Thriller", 293))
        self.add_music(Music("mu3", "Back in Black", ["Rock", "Hard Rock"], 1980, 9.0, 
                            "AC/DC", "Back in Black", 255))
        self.add_music(Music("mu4", "After Hours", ["R&B", "Pop"], 2020, 8.7, 
                            "The Weeknd", "After Hours", 214))
        self.add_music(Music("mu5", "folklore", ["Alternative", "Pop"], 2020, 8.9, 
                            "Taylor Swift", "folklore", 246))
        
        # Sample Books
        self.add_book(Book("b1", "To Kill a Mockingbird", ["Fiction", "Classic"], 1960, 9.2, 
                          "Harper Lee", 281, "J. B. Lippincott & Co."))
        self.add_book(Book("b2", "1984", ["Dystopian", "Science Fiction"], 1949, 9.1, 
                          "George Orwell", 328, "Secker & Warburg"))
        self.add_book(Book("b3", "The Lord of the Rings", ["Fantasy", "Adventure"], 1954, 9.3, 
                          "J.R.R. Tolkien", 1178, "Allen & Unwin"))
        self.add_book(Book("b4", "The Hunger Games", ["Dystopian", "Science Fiction", "Young Adult"], 2008, 8.6, 
                          "Suzanne Collins", 374, "Scholastic"))
        self.add_book(Book("b5", "Educated", ["Memoir", "Biography"], 2018, 8.9, 
                          "Tara Westover", 334, "Random House"))
        
        # Sample Games
        self.add_game(Game("g1", "The Legend of Zelda: Breath of the Wild", ["Action", "Adventure"], 2017, 9.5, 
                          "Nintendo", ["Nintendo Switch", "Wii U"], False))
        self.add_game(Game("g2", "The Witcher 3: Wild Hunt", ["Action", "RPG"], 2015, 9.4, 
                          "CD Projekt Red", ["PC", "PlayStation 4", "Xbox One", "Nintendo Switch"], False))
        self.add_game(Game("g3", "Fortnite", ["Battle Royale", "Survival"], 2017, 8.8, 
                          "Epic Games", ["PC", "PlayStation", "Xbox", "Nintendo Switch", "Mobile"], True))
        self.add_game(Game("g4", "Red Dead Redemption 2", ["Action", "Adventure"], 2018, 9.7, 
                          "Rockstar Games", ["PlayStation 4", "Xbox One", "PC"], True))
        self.add_game(Game("g5", "Minecraft", ["Sandbox", "Survival"], 2011, 9.3, 
                          "Mojang", ["PC", "Console", "Mobile"], True))
    
    def add_movie(self, movie: Movie):
        self.movies[movie.item_id] = movie
    
    def add_music(self, music: Music):
        self.music[music.item_id] = music
    
    def add_book(self, book: Book):
        self.books[book.item_id] = book
    
    def add_game(self, game: Game):
        self.games[game.item_id] = game
    
    def get_movies(self) -> List[Movie]:
        return list(self.movies.values())
    
    def get_music(self) -> List[Music]:
        return list(self.music.values())
    
    def get_books(self) -> List[Book]:
        return list(self.books.values())
    
    def get_games(self) -> List[Game]:
        return list(self.games.values())
    
    def get_movie_by_id(self, movie_id: str) -> Optional[Movie]:
        return self.movies.get(movie_id)
    
    def get_music_by_id(self, music_id: str) -> Optional[Music]:
        return self.music.get(music_id)
    
    def get_book_by_id(self, book_id: str) -> Optional[Book]:
        return self.books.get(book_id)
    
    def get_game_by_id(self, game_id: str) -> Optional[Game]:
        return self.games.get(game_id)
    
    def save_to_file(self, filename: str = "entertainment_db.json"):
        """Save the database to a JSON file."""
        data = {
            "movies": {k: v.to_dict() for k, v in self.movies.items()},
            "music": {k: v.to_dict() for k, v in self.music.items()},
            "books": {k: v.to_dict() for k, v in self.books.items()},
            "games": {k: v.to_dict() for k, v in self.games.items()}
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
    
    def load_from_file(self, filename: str = "entertainment_db.json"):
        """Load the database from a JSON file."""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            # Clear current data
            self.movies = {}
            self.music = {}
            self.books = {}
            self.games = {}
            
            # Load movies
            for movie_id, movie_data in data.get("movies", {}).items():
                self.add_movie(Movie(
                    movie_data["id"],
                    movie_data["title"],
                    movie_data["genre"],
                    movie_data["year"],
                    movie_data["rating"],
                    movie_data["director"],
                    movie_data["actors"],
                    movie_data["duration"]
                ))
            
            # Load music
            for music_id, music_data in data.get("music", {}).items():
                self.add_music(Music(
                    music_data["id"],
                    music_data["title"],
                    music_data["genre"],
                    music_data["year"],
                    music_data["rating"],
                    music_data["artist"],
                    music_data.get("album"),
                    music_data.get("duration")
                ))
            
            # Load books
            for book_id, book_data in data.get("books", {}).items():
                self.add_book(Book(
                    book_data["id"],
                    book_data["title"],
                    book_data["genre"],
                    book_data["year"],
                    book_data["rating"],
                    book_data["author"],
                    book_data["pages"],
                    book_data["publisher"]
                ))
            
            # Load games
            for game_id, game_data in data.get("games", {}).items():
                self.add_game(Game(
                    game_data["id"],
                    game_data["title"],
                    game_data["genre"],
                    game_data["year"],
                    game_data["rating"],
                    game_data["developer"],
                    game_data["platforms"],
                    game_data["multiplayer"]
                ))
            
            return True
        except Exception as e:
            print(f"Error loading database: {e}")
            return False


class RecommendationEngine:
    """Class to generate personalized recommendations."""
    def __init__(self, database: EntertainmentDatabase):
        self.db = database
    
    def calculate_match_score(self, item: EntertainmentItem, user: UserProfile, media_type: str) -> float:
        """Calculate how well an item matches user preferences."""
        score = 0.0
        
        # Base score on rating
        score += item.rating / 10.0  # Convert to 0-1 scale
        
        # Check genres
        user_genres = user.preferences[media_type]["genres"]
        for genre in item.genre:
            if genre in user_genres:
                score += 0.3
        
        # Check years
        user_years = user.preferences[media_type]["years"]
        if item.year in user_years:
            score += 0.2
        elif any(abs(item.year - year) <= 5 for year in user_years):
            score += 0.1
        
        # Check item-specific characteristics
        if media_type == "movie":
            # Check directors
            if item.director in user.preferences["movie"]["directors"]:
                score += 0.2
            
            # Check actors
            for actor in item.actors:
                if actor in user.preferences["movie"]["actors"]:
                    score += 0.15
        
        elif media_type == "music":
            # Check artists
            if item.artist in user.preferences["music"]["artists"]:
                score += 0.4
        
        elif media_type == "book":
            # Check authors
            if item.author in user.preferences["book"]["authors"]:
                score += 0.4
        
        elif media_type == "game":
            # Check developers
            if item.developer in user.preferences["game"]["developers"]:
                score += 0.2
            
            # Check platforms
            for platform in item.platforms:
                if platform in user.preferences["game"]["platforms"]:
                    score += 0.2
                    break
        
        # Penalize already consumed items
        if item.item_id in user.history[media_type]:
            score -= 1.0
        
        return score
    
    def get_recommendations(self, user: UserProfile, media_type: str, count: int = 3) -> List[Dict]:
        """Get personalized recommendations for a specific media type."""
        all_items = []
        
        if media_type == "movie":
            all_items = self.db.get_movies()
        elif media_type == "music":
            all_items = self.db.get_music()
        elif media_type == "book":
            all_items = self.db.get_books()
        elif media_type == "game":
            all_items = self.db.get_games()
        
        # Calculate match scores
        scored_items = [(item, self.calculate_match_score(item, user, media_type)) for item in all_items]
        
        # Sort by score and take top 'count' items
        scored_items.sort(key=lambda x: x[1], reverse=True)
        top_items = [item.to_dict() for item, score in scored_items[:count]]
        
        return top_items
    
    def get_trending(self, media_type: str, count: int = 3) -> List[Dict]:
        """Get current trending items for a specific media type."""
        # In a real app, this would use actual trending data
        # For now, we'll simulate trending by taking the newest and highest rated items
        
        all_items = []
        if media_type == "movie":
            all_items = self.db.get_movies()
        elif media_type == "music":
            all_items = self.db.get_music()
        elif media_type == "book":
            all_items = self.db.get_books()
        elif media_type == "game":
            all_items = self.db.get_games()
        
        # Sort by a combination of year (newer) and rating (higher)
        current_year = datetime.now().year
        scored_items = [(item, (current_year - item.year) * 0.1 + item.rating) for item in all_items]
        scored_items.sort(key=lambda x: x[1], reverse=True)
        
        trending_items = [item.to_dict() for item, score in scored_items[:count]]
        return trending_items


class EntertainmentAIAgent:
    """Main AI agent class to handle user interactions and recommendations."""
    def __init__(self):
        self.db = EntertainmentDatabase()
        self.recommendation_engine = RecommendationEngine(self.db)
        self.users = {}
        self.current_user = None
    
    def load_data(self, db_filename: str = "entertainment_db.json", users_filename: str = "users.json"):
        """Load database and user data from files."""
        self.db.load_from_file(db_filename)
        
        try:
            with open(users_filename, 'r') as f:
                users_data = json.load(f)
            
            for user_id, user_data in users_data.items():
                self.users[user_id] = UserProfile.from_dict(user_data)
            
            return True
        except Exception as e:
            print(f"Error loading users: {e}")
            return False
    
    def save_data(self, db_filename: str = "entertainment_db.json", users_filename: str = "users.json"):
        """Save database and user data to files."""
        self.db.save_to_file(db_filename)
        
        users_data = {user_id: user.to_dict() for user_id, user in self.users.items()}
        with open(users_filename, 'w') as f:
            json.dump(users_data, f, indent=4)
    
    def create_user(self, name: str) -> str:
        """Create a new user profile."""
        user_id = f"user_{len(self.users) + 1}"
        self.users[user_id] = UserProfile(user_id, name)
        self.current_user = user_id
        return user_id
    
    def set_current_user(self, user_id: str) -> bool:
        """Set the current active user."""
        if user_id in self.users:
            self.current_user = user_id
            return True
        return False
    
    def add_user_preference(self, media_type: str, category: str, value: Union[str, int, float]) -> bool:
        """Add a preference to the current user's profile."""
        if not self.current_user:
            return False
        
        self.users[self.current_user].add_preference(media_type, category, value)
        return True
    
    def add_to_history(self, media_type: str, item_id: str) -> bool:
        """Add an item to the current user's history."""
        if not self.current_user:
            return False
        
        self.users[self.current_user].add_to_history(media_type, item_id)
        return True
    
    def get_recommendations(self, media_type: str = None, count: int = 3) -> Dict:
        """Get personalized recommendations for the current user."""
        if not self.current_user:
            return {"error": "No user selected"}
        
        user = self.users[self.current_user]
        
        recommendations = {}
        
        if media_type:
            # Get recommendations for specific media type
            if media_type in ["movie", "music", "book", "game"]:
                recommendations[media_type] = self.recommendation_engine.get_recommendations(user, media_type, count)
        else:
            # Get recommendations for all media types
            recommendations["movies"] = self.recommendation_engine.get_recommendations(user, "movie", count)
            recommendations["music"] = self.recommendation_engine.get_recommendations(user, "music", count)
            recommendations["books"] = self.recommendation_engine.get_recommendations(user, "book", count)
            recommendations["games"] = self.recommendation_engine.get_recommendations(user, "game", count)
        
        return recommendations
    
    def get_trending(self, media_type: str = None, count: int = 3) -> Dict:
        """Get trending items."""
        trending = {}
        
        if media_type:
            # Get trending items for specific media type
            if media_type in ["movie", "music", "book", "game"]:
                trending[media_type] = self.recommendation_engine.get_trending(media_type, count)
        else:
            # Get trending items for all media types
            trending["movies"] = self.recommendation_engine.get_trending("movie", count)
            trending["music"] = self.recommendation_engine.get_trending("music", count)
            trending["books"] = self.recommendation_engine.get_trending("book", count)
            trending["games"] = self.recommendation_engine.get_trending("game", count)
        
        return trending
    
    def search(self, query: str, media_type: str = None) -> Dict:
        """Search for entertainment items matching the query."""
        results = {}
        query = query.lower()
        
        def matches_query(item):
            """Check if an item matches the search query."""
            if query in item.title.lower():
                return True
            
            for genre in item.genre:
                if query in genre.lower():
                    return True
            
            return False
        
        if media_type == "movie" or media_type is None:
            movie_results = [movie.to_dict() for movie in self.db.get_movies() if matches_query(movie)]
            if movie_results:
                results["movies"] = movie_results
        
        if media_type == "music" or media_type is None:
            music_results = [music.to_dict() for music in self.db.get_music() if matches_query(music)]
            if music_results:
                results["music"] = music_results
        
        if media_type == "book" or media_type is None:
            book_results = [book.to_dict() for book in self.db.get_books() if matches_query(book)]
            if book_results:
                results["books"] = book_results
        
        if media_type == "game" or media_type is None:
            game_results = [game.to_dict() for game in self.db.get_games() if matches_query(game)]
            if game_results:
                results["games"] = game_results
        
        return results


# Example usage of the Entertainment AI Agent
def main():
    # Initialize the agent
    agent = EntertainmentAIAgent()
    
    # Create a user
    user_id = agent.create_user("John")
    
    # Add some preferences
    agent.add_user_preference("movie", "genres", "Sci-Fi")
    agent.add_user_preference("movie", "genres", "Action")
    agent.add_user_preference("movie", "actors", "Leonardo DiCaprio")
    
    agent.add_user_preference("music", "genres", "Rock")
    agent.add_user_preference("music", "artists", "Queen")
    
    agent.add_user_preference("book", "genres", "Fantasy")
    agent.add_user_preference("book", "authors", "J.R.R. Tolkien")
    
    agent.add_user_preference("game", "genres", "Action")
    agent.add_user_preference("game", "platforms", "PC")
    
    # Get recommendations
    recommendations = agent.get_recommendations()
    
    print("Personalized Recommendations for", agent.users[user_id].name)
    print("\nMovies:")
    for movie in recommendations.get("movies", []):
        print(f"- {movie['title']} ({movie['year']}) - {', '.join(movie['genre'])}")
    
    print("\nMusic:")
    for music in recommendations.get("music", []):
        print(f"- {music['title']} by {music['artist']} ({music['year']}) - {', '.join(music['genre'])}")
    
    print("\nBooks:")
    for book in recommendations.get("books", []):
        print(f"- {book['title']} by {book['author']} ({book['year']}) - {', '.join(book['genre'])}")
    
    print("\nGames:")
    for game in recommendations.get("games", []):
        print(f"- {game['title']} by {game['developer']} ({game['year']}) - {', '.join(game['genre'])}")
    
    # Get trending items
    trending = agent.get_trending()
    
    print("\nTrending Entertainment:")
    print("\nMovies:")
    for movie in trending.get("movies", []):
        print(f"- {movie['title']} ({movie['year']}) - {', '.join(movie['genre'])}")
    
    # Search for something
    print("\nSearch results for 'action':")
    search_results = agent.search("action")
    
    for media_type, items in search_results.items():
        print(f"\n{media_type.capitalize()}:")
        for item in items:
            print(f"- {item['title']} ({item['year']}) - {', '.join(item['genre'])}")
    
    # Save data
    agent.save_data()


if __name__ == "__main__":
    main()